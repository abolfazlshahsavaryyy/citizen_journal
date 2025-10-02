using Carter;
using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using SaveNews.Models;
using SaveNews.Handler.CreateSaveNews;
public class SaveNewsModule : CarterModule
{
    public override void AddRoutes(IEndpointRouteBuilder app)
    {
        var saveNewsGroup = app.MapGroup("/save-news")
                               .RequireAuthorization(); // JWT required

        saveNewsGroup.MapPost("", async (HttpContext context, IMediator mediator) =>
        {
            // Read JSON body
            var request = await context.Request.ReadFromJsonAsync<SaveNewsRequest>();
            if (request == null) return Results.BadRequest();

            // Extract UserId from JWT claims
            var userIdClaim = context.User.Claims.FirstOrDefault(c => c.Type == "user_id");
            if (userIdClaim == null) return Results.Unauthorized();

            int userId = int.Parse(userIdClaim.Value);

            // Create command
            var command = new SaveNewsCommand(request.NewsId, request.TextContent, userId);

            // Send command to MediatR
            var result = await mediator.Send(command);

            return Results.Ok(result);
        });
    }
}

// DTO for request
public record SaveNewsRequest(int NewsId, string TextContent);
