using ShareNewsGrpc.Data;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

//for deploy development
// var dbUser = Environment.GetEnvironmentVariable("DB_USER") ?? "sa";
// var dbPassword = Environment.GetEnvironmentVariable("SA_PASSWORD") ?? "YourStrong@Passw0rd";
// var dbName = Environment.GetEnvironmentVariable("DB_NAME") ?? "GrpcDemoDb";
// var dbPort = Environment.GetEnvironmentVariable("DB_PORT") ?? "1433";

// var connectionString = $"Server=localhost,{dbPort};Database={dbName};User Id={dbUser};Password={dbPassword};";

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddGrpc();

var app = builder.Build();
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();   // Apply migrations
    DbInitializer.Seed(db);  // Seed data
}

// Configure the HTTP request pipeline.
app.MapGrpcService<ShareNewsServiceImpl>();

app.MapGet("/", () => "Communication with gRPC endpoints must be made through a gRPC client. To learn how to create a client, visit: https://go.microsoft.com/fwlink/?linkid=2086909");

app.Run();
