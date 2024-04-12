FROM --platform=linux/x86_64 golang:1.22
#FROM --platform=aarch64 golang:1.22
#FROM golang:1.22
RUN mkdir /app
ADD . /app/
RUN cd /app/pkg/ml/catboost/catboost/libs && \
    tar -xzvf libcatboostmodel.tar.gz -C /app/pkg/ml/catboost/catboost/libs/model_interface
WORKDIR /app/internal/app/cb-api
#ENV LD_LIBRARY_PATH=/app/pkg/ml/catboost/catboost/libs/model_interface
RUN go build -o /cb-api
CMD ["/cb-api"]

