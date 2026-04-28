def rle_encode(data: bytes, Ms=1, Mc=1) -> bytes:
    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        # считаем длину повтора
        run_len = 1
        while (i + run_len < n and
               data[i:i+Ms] == data[i+run_len:i+run_len+Ms] and
               run_len < 127):
            run_len += 1

        if run_len > 1:
            result.append(run_len)
            result.extend(data[i:i+Ms])
            i += run_len
        else:
            # сырой блок
            start = i
            raw_len = 1

            while i + raw_len < n and raw_len < 127:
                # проверяем, начинается ли повтор
                lookahead_run = 1
                while (i + raw_len + lookahead_run < n and
                       data[i+raw_len:i+raw_len+Ms] ==
                       data[i+raw_len+lookahead_run:i+raw_len+lookahead_run+Ms] and
                       lookahead_run < 127):
                    lookahead_run += 1

                if lookahead_run > 1:
                    break

                raw_len += 1

            result.append(0x80 | raw_len)
            result.extend(data[i:i+raw_len])
            i += raw_len

    return bytes(result)

def rle_decode(data: bytes, Ms=1, Mc=1) -> bytes:
    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        control = data[i]
        i += 1

        if control & 0x80:
            # сырая последовательность
            length = control & 0x7F
            result.extend(data[i:i+length])
            i += length
        else:
            # повтор
            length = control
            symbol = data[i:i+Ms]
            i += Ms
            result.extend(symbol * length)

    return bytes(result)