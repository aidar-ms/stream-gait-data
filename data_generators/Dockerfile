FROM aidarms/stream-gait:latest

RUN curl -L https://springernature.figshare.com/ndownloader/files/21998373 --output input_data_SD.zip
# RUN curl https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-zip-file.zip --output input_data_SD.zip
RUN unzip -o input_data_SD.zip
RUN mv "input data_SD" input_data_SD
RUN rm input_data_SD.zip

COPY generate_surface_gait_data.py ./generate_surface_gait_data.py
COPY records ./records

ENV PYTHONPATH ${PYTHONPATH}:.

CMD ["python", "generate_surface_gait_data.py", "-kh", "broker:9092", "-p", "1,2,3,4,5"]