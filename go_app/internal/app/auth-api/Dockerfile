FROM golang:1.22
RUN mkdir /app
ADD . /app/
WORKDIR /app/internal/app/auth-api
RUN go build -o /auth-api
CMD ["/auth-api"]