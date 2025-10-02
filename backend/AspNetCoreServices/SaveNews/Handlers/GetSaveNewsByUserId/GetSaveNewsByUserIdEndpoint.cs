using Carter;
using MediatR;
using Microsoft.AspNetCore.Http;
using SaveNews.Handler.CreateSaveNews;
using SaveNews.Handler.GetSavedNews;
using SaveNews.Models;

public class GetSaveNewsByUserIdModule : CarterModule
{
    public override void AddRoutes(IEndpointRouteBuilder app)
    {
        var saveNewsGroup = app.MapGroup("/save-news")
                               .RequireAuthorization(); // JWT required

        // GET - get all saved news for the current user
        saveNewsGroup.MapGet("", async (HttpContext context, IMediator mediator) =>
        {
            var userIdClaim = context.User.Claims.FirstOrDefault(c => c.Type == "user_id");
            if (userIdClaim == null) return Results.Unauthorized();

            if (!int.TryParse(userIdClaim.Value, out var userId))
                return Results.Unauthorized();

            var query = new GetSavedNewsQuery(userId);
            var result = await mediator.Send(query);

            return Results.Ok(result);
        });
    }
}

