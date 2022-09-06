FROM golang:1.16.4-alpine3.13 AS builder
WORKDIR /go/src
COPY ./ .
RUN go env -w GO111MODULE=on \
    && go env -w GOPROXY=https://goproxy.cn,direct \
    && go env -w CGO_ENABLED=0 \
    && go env \
    && go mod tidy \
    && go build -o mysql_exporter .

# runtime
FROM alpine:latest
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories &&\
    apk update --no-cache && apk add ca-certificates --no-cache && \
    apk add tzdata --no-cache && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
COPY --from=builder /go/src/mysql_exporter /mysql_exporter
EXPOSE 8090
ENTRYPOINT ["/mysql_exporter"]