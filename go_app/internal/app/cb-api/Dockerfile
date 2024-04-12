FROM --platform=aarch64 golang:1.22
#FROM golang:1.22
RUN mkdir /app
ADD . /app/
WORKDIR /app/internal/app/cb-api
#ENV LD_LIBRARY_PATH=/app/pkg/ml/catboost/catboost/libs/model_interface
RUN go build -o /cb-api
CMD ["/cb-api"]

