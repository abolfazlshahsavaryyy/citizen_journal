# Step 1: Use the official .NET SDK image for building
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore as distinct layers
COPY ShareNewsGrpc.csproj .
RUN dotnet restore ShareNewsGrpc.csproj

# Copy everything else and build
COPY . .
RUN dotnet publish ShareNewsGrpc.csproj -c Release -o /app/publish

# Step 2: Use ASP.NET runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "ShareNewsGrpc.dll"]
