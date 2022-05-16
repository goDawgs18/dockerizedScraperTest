# FROM public.ecr.aws/lambda/python@sha256:75dd3378f9733d43f4a4b6a02c237512e0c6de583464f7abf4c4507aec90cf48 as build
# RUN yum install -y unzip && \
#     curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip" && \
#     curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F982481%2Fchrome-linux.zip?alt=media" && \
#     unzip /tmp/chromedriver.zip -d /opt/ && \
#     unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python:3.9
# RUN pip install selenium
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F982481%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y


# COPY --from=build /opt/chrome-linux /opt/chrome
# COPY --from=build /opt/chromedriver /opt/
COPY . .

RUN yum install tree -y && tree /opt && tree .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "v5.handler" ]