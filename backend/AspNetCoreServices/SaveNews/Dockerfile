# Step 1: Build image
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY SaveNews.csproj .
RUN dotnet restore SaveNews.csproj

# Copy everything and build
COPY . .
RUN dotnet publish SaveNews.csproj -c Release -o /app/publish

# Step 2: Runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

# Expose port (choose a different one if 8080 is taken)
EXPOSE 8090

ENTRYPOINT ["dotnet", "SaveNews.dll"]
