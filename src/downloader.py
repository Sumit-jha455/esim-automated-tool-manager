import os
import urllib.request
import py7zr

from logger import logger


class ToolDownloader:

    @staticmethod
    def download_and_extract(
        url,
        archive_name,
        extract_directory
    ):
        """
        Download a .7z archive and extract it.
        """

        os.makedirs(extract_directory, exist_ok=True)

        archive_path = os.path.join(
            extract_directory,
            archive_name
        )

        try:
            logger.info(
                "Downloading archive from: %s",
                url
            )

            print("\nDownloading Ngspice package...")
            print(f"Source: {url}")

            urllib.request.urlretrieve(
                url,
                archive_path
            )

            logger.info(
                "Download completed: %s",
                archive_path
            )

            print("✓ Download completed.")

            print("\nExtracting package...")

            with py7zr.SevenZipFile(
                archive_path,
                mode="r"
            ) as archive:

                archive.extractall(
                    path=extract_directory
                )

            logger.info(
                "Archive extracted to: %s",
                extract_directory
            )

            print("✓ Extraction completed.")

            return True, extract_directory

        except Exception as error:

            logger.error(
                "Download/extraction failed: %s",
                error
            )

            return False, str(error)

        finally:

            # Remove downloaded archive after extraction
            if os.path.exists(archive_path):

                try:
                    os.remove(archive_path)

                    logger.info(
                        "Temporary archive removed."
                    )

                except Exception as error:

                    logger.warning(
                        "Could not remove archive: %s",
                        error
                    )