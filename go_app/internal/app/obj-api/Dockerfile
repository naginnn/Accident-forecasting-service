FROM golang:1.22
RUN mkdir /app
ADD . /app/
WORKDIR /app/internal/app/obj-api
RUN go build -o /obj-api
CMD ["/obj-api"]