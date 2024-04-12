FROM --platform=linux/x86_64 golang:1.22
#FROM --platform=aarch64 golang:1.22
#FROM golang:1.22
RUN mkdir /app
ADD . /app/
RUN cd /app/pkg/ml/catboostlib && \
    tar -xzvf libcatboostmodel.tar.gz && \
    mv libcatboostmodel.so.1 libcatboostmodel.so /usr/lib
WORKDIR /app/internal/app/cb-api
RUN go build -o /cb-api
CMD ["/cb-api"]

