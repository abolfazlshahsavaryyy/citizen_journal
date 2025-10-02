using Microsoft.EntityFrameworkCore;
using SaveNews.Data;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Net.Http;
using System.Security.Cryptography;
using SaveNews.Handler.CreateSaveNews; 
using Carter;
using MediatR;


var builder = WebApplication.CreateBuilder(args);


//configure the ef core for sqlite
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

//configure the http route to Django app
builder.Services.AddHttpClient("PublicKeyClient", client =>
{
    client.BaseAddress = new Uri("http://localhost:8000/");
});
//configure mediatR for CQRS
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(SaveNewsCommandHandler).Assembly));


// Fetch the public key from Django
using var httpClient = new HttpClient();
var publicKeyText = await httpClient.GetStringAsync("http://localhost:8000/account/api/public-key/");

// Import into RSA
using var rsa = RSA.Create();
rsa.ImportFromPem(publicKeyText.ToCharArray());

var key = new RsaSecurityKey(rsa);

// Configure JWT authentication
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = false,
        ValidateAudience = false,
        ValidateLifetime = true,
        RequireExpirationTime = true,
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = key,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();
builder.Services.AddCarter();
var app = builder.Build();


app.UseAuthentication();
app.UseAuthorization();

app.MapCarter();


app.Run();
