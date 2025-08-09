FROM alpine:3.20

RUN apk add --no-cache bash grep wget curl

# MinIO Client (mc) indir ve kur
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/bin/mc \
    && chmod +x /usr/bin/mc

#COPY minio/public-policy.json /tmp/public-policy.json
COPY minio/replicate.json /tmp/replicate.json

ENTRYPOINT ["mc"]