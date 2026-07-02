# async-net-probe
async-net-probe: A high-performance async TCP port scanner &amp; banner grabber in pure Python. Uses non-blocking socket multiplexing via asyncio to audit 1000+ ports in under 1.5s with zero external dependencies. Features active HTTP protocol injection for silent targets and strict resource boundaries to prevent OS socket exhaustion.
# async-net-probe

### Installation Guide
1. Open Crostini terminal
2. Clone tool: `git clone https://github.com/sweetcookiecake/async-net-probe/`
3. Enter folder: `cd async-net-probe`

### Usage
- Scan web target: `python3 scanner/core.py google.com`
- Scan local sandbox: `python3 scanner/core.py 127.0.0.1 -p 1-500`
