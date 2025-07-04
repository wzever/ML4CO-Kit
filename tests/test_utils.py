import os
import sys
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
import shutil
from ml4co_kit.utils.file_utils import (
    compress_folder, extract_archive, pull_file_from_huggingface
)


def test_file_utils():
    # compress .tar.gz
    compress_folder(
        folder="tests/data_for_tests/utils/extract_compress",
        compress_path="tests/data_for_tests/utils/extract_compress.tar.gz"
    )
    shutil.rmtree("tests/data_for_tests/utils/extract_compress")
    
    # extract_archive .tar.gz
    extract_archive(
        archive_path="tests/data_for_tests/utils/extract_compress.tar.gz",
        extract_path="tests/data_for_tests/utils/extract_compress"
    )
    os.remove("tests/data_for_tests/utils/extract_compress.tar.gz")
    
    # compress .zip
    compress_folder(
        folder="tests/data_for_tests/utils/extract_compress",
        compress_path="tests/data_for_tests/utils/extract_compress.zip"
    )
    shutil.rmtree("tests/data_for_tests/utils/extract_compress")
    
    # extract_archive .zip
    extract_archive(
        archive_path="tests/data_for_tests/utils/extract_compress.zip",
        extract_path="tests/data_for_tests/utils/extract_compress"
    )
    os.remove("tests/data_for_tests/utils/extract_compress.zip")

    # pull file from huggingface
    pull_file_from_huggingface(
        repo_id="ML4CO/ML4CO-Kit", 
        repo_type="model", 
        filename="neurolkh/neurolkh_original.pt", 
        save_path="tmp/neurolkh_original.pt"
    )
    shutil.rmtree("tmp")


if __name__ == "__main__":
    test_file_utils()
