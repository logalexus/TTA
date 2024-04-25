import pyshark


class AsyncLiveCapture(pyshark.LiveCapture):
    async def sniff_continuously(self, packet_count=None):
        tshark_process = await self._get_tshark_process()
        packets_captured = 0
        parser = self._setup_tshark_output_parser()

        data = b''
        try:
            while True:
                try:
                    packet, data = await parser.get_packets_from_stream(tshark_process.stdout, data,
                                                                        got_first_packet=packets_captured > 0)
                except EOFError:
                    self._log.debug('EOF reached (sync)')
                    self._eof_reached = True
                    break

                if packet:
                    packets_captured += 1
                    yield packet
                if packet_count and packets_captured >= packet_count:
                    break
        finally:
            if tshark_process in self._running_processes:
                await self._cleanup_subprocess(tshark_process)