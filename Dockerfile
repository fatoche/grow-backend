FROM condaforge/mambaforge:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Copy environment file first for better caching
COPY environment.yaml .

# Create and activate conda environment
RUN mamba env create -f environment.yaml -n grow-backend && \
    mamba clean --all --yes && \
    echo "mamba activate grow-backend" >> ~/.bashrc

# Activate the environment for subsequent RUN commands
ENV PATH /opt/conda/envs/grow-backend/bin:$PATH

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
