FROM public.ecr.aws/x8v8d7g8/mars-base:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["/bin/bash"]

