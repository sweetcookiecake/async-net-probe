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
- Async-Net-Probe (Python, Git, Linux/Crostini)Engineered a high-performance network discovery tool utilizing an asynchronous event-driven loop architecture to audit 1,000+ TCP ports in under 1.5 seconds.Implemented socket multiplexing and an active protocol probing engine to capture live application-layer service banners.Managed operating system constraints by integrating concurrent semaphore pools to eliminate file descriptor exhaustion.
