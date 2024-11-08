  #!/bin/bash

  echo "Building Users Guide from TIFFs"
  echo "Formating TIFF's to correct scanning errors - omitting cover and back page"

  # build pdf
  python3 ./script/tiff_to_pdf.py ./tiffs ./pdf/SOS_Small_Computer_Operating_System_Users_Guide_Soistmann_Enterprises.pdf


  echo "You can safely ignore the OCR issues on page 50 as this is a hand written recipt."
  echo "have a nice day!"

