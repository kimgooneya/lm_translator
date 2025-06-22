from my_local_llm import MyLocalLLM
from pdf_reader import PDFReader


def main():
    print("Hello from lm-translator!")
    myllm = MyLocalLLM('qwen/qwen3-8b')
    mypdfreader= PDFReader("filepath.pdf")
    print(mypdfreader.read_pages_with_pypdf2())

    

if __name__ == "__main__":
    main()
