using Carter;
using Microsoft.AspNetCore.Authorization;

public class HelloModule : CarterModule
{
    public override void AddRoutes(IEndpointRouteBuilder app)
    {
        // Require authentication
        var authorizedGroup = app.MapGroup("/hello")
                                 .RequireAuthorization(); // This ensures JWT auth is required

        // Define GET endpoint
        authorizedGroup.MapGet("", async context =>
        {
            await context.Response.WriteAsync("Hello from Carter!");
        });
    }
}
