from unstructured.partition.pdf import partition_pdf
import os
import time

class PDFProcessor:
    def __init__(self, input_folder):
      self.input_folder = os.path.abspath(os.path.join(os.getcwd(), input_folder))
      self.all_pdf_data = {}
      self.concatenated_pdf_data = []

    def read_pdf(self, pdf_file_path):
        try:
            if not os.path.exists(pdf_file_path) or not pdf_file_path.endswith('.pdf'):
                print(f"PDF file not found or invalid format: {pdf_file_path}")
                return None

            # Extract details from the PDF using partition_pdf
            pdf_raw_data = partition_pdf(
                filename=pdf_file_path,
                strategy="hi_res",
                extract_images_in_pdf=True,
                extract_image_block_to_payload=False,
                extract_image_block_output_dir="./data1/images1/"
            )

            return pdf_raw_data

        except Exception as e:
            print(f"Error in read_pdf: {str(e)}")
            return None

    def read_multiple_files(self):
        try:
            if not os.path.exists(self.input_folder) or not os.path.isdir(self.input_folder):
                print(f"Folder not found or is not a directory: {self.input_folder}")
                return None

            pdf_files = [file for file in os.listdir(self.input_folder) if file.endswith('.pdf')]

            for pdf_file in pdf_files:
                pdf_file_path = os.path.join(self.input_folder, pdf_file)
                print(f"Processing file: {pdf_file_path}")
                start_time = time.time()

                pdf_data = self.read_pdf(pdf_file_path)
                print(f"Successfully processed pdf file: {pdf_file_path}")

                # End measuring the time
                processing_time_seconds = time.time() - start_time
                minutes, seconds = divmod(processing_time_seconds, 60)

                # Get the file size
                file_size_bytes = os.path.getsize(pdf_file_path)
                file_size_mb = file_size_bytes / (1024 * 1024)

                if pdf_data is not None:
                   self.all_pdf_data[pdf_file] = {
                        "pdf_file_path": pdf_file_path,
                        "pdf_data": pdf_data,
                        "processing_time": f"{int(minutes)} min and {int(seconds)} sec",
                        "file_size_mb": round(file_size_mb, 3)
                    }
                else:
                    print(f"Failed to process file: {pdf_file_path}")

            return self.all_pdf_data, self.concatenated_pdf_data

        except Exception as e:
            print(f"Error in read_multiple_files: {str(e)}")
            return None
