from ctypes import cdll
lib = cdll.LoadLibrary('./LineReader.so')

class ReadLine:
    @staticmethod
    def readline(line: int):
        return lib.getLineString(line)

if __name__ == "__main__":
    print(ReadLine.readline(2132))