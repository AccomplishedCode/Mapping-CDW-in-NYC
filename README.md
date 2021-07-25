# Mapping-CDW-in-NYC
This is a Capstone Project for my program at NYU Center for Urban Sciences & Progress. Commissioned by the Town+Gown Committee of the NYC government, the project aims to map all the construction and demolition waste occuring in NYC. The goal was to map not just the flow of materials, but also breaking down trips by material, weight as well as regions. 

### Preprocessing

The data we worked with was in the form of scanned handwritten PDF forms. Obviously this meant we had to come up with an OCR technique to scan and read all the forms. We used Tesseract OCR + Google Vision to extract data, a lot of regex magic, as well as custom rules to sort the data values as well as embedding them in the right column.In some cases, the data was manually entered to ensure accuracy. 

### Mapping

The mapping was done using the excellent Pydeck module, and hosted via Streamlit. 

### Project link

The project can be found here: 

https://share.streamlit.io/accomplishedcode/mapping-cdw-in-nyc/main/main.py
