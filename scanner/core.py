import asyncio
import socket
import sys
import time
import argparse

class AsyncPortScanner:
    def __init__(self, target_host: str, max_concurrent_tasks: int = 200, timeout: float = 1.0):
        self.target_host = target_host
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def _probe_active_service(self, reader, writer, port: int) -> str:
        try:
            # FIXED: Added the specific web ports to check against
            if port in [80, 443, 8080]:
                writer.write(b"HEAD / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
                await writer.drain()
            banner_bytes = await asyncio.wait_for(reader.read(512), timeout=1.0)
            if banner_bytes:
                return banner_bytes.decode('utf-8', errors='ignore').strip().split('\n')[0]
        except (asyncio.TimeoutError, OSError):
            pass
        return "Open (No banner returned)"

    async def scan_single_port(self, port: int) -> dict:
        async with self.semaphore:
            result = {"port": port, "status": "closed", "banner": None}
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.target_host, port),
                    timeout=self.timeout
                )
                result["status"] = "open"
                try:
                    banner_bytes = await asyncio.wait_for(reader.read(512), timeout=0.5)
                    if banner_bytes:
                        result["banner"] = banner_bytes.decode('utf-8', errors='ignore').strip().split('\n')[0]
                except asyncio.TimeoutError:
                    result["banner"] = await self._probe_active_service(reader, writer, port)
                writer.close()
                await writer.wait_closed()
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                pass
            return result

    async def execute_scan(self, ports: list[int]) -> list[dict]:
        print(f"[*] Target Scope: {self.target_host}", file=sys.stderr)
        print(f"[*] Dispatching tasks over {len(ports)} target ports...", file=sys.stderr)
        start_time = time.perf_counter()
        
        tasks = [self.scan_single_port(port) for port in ports]
        scan_results = await asyncio.gather(*tasks)
        
        open_ports = [res for res in scan_results if res["status"] == "open"]
        elapsed = time.perf_counter() - start_time
        print(f"[+] Audit complete in {elapsed:.2f}s. Discovered {len(open_ports)} exposed entry points.\n", file=sys.stderr)
        return open_ports

def main():
    parser = argparse.ArgumentParser(description="Enterprise Asynchronous Port Scanner.")
    parser.add_argument("target", help="Target IP address or domain")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range 'start-end' (Default: 1-1024)")
    parser.add_argument("-w", "--workers", type=int, default=200, help="Max concurrent connections")
    
    args = parser.parse_args()
    
    try:
        start_p, end_p = map(int, args.ports.split("-"))
        port_list = list(range(start_p, end_p + 1))
    except ValueError:
        print("[!] Error: Invalid port range format. Use '1-1000'.", file=sys.stderr)
        sys.exit(1)

    scanner = AsyncPortScanner(target_host=args.target, max_concurrent_tasks=args.workers)
    
    try:
        results = asyncio.run(scanner.execute_scan(port_list))
        print(f"{'PORT':<8} | {'STATUS':<8} | {'IDENTIFIED BANNER / SERVICE METADATA'}")
        print("-" * 70)
        for item in results:
            print(f"{item['port']:<8} | {item['status']:<8} | {item['banner']}")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by operator.", file=sys.stderr)

if __name__ == "__main__":
    main()
