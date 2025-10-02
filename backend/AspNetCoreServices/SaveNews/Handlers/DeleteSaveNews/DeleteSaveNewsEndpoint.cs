using Carter;
using MediatR;
using Microsoft.AspNetCore.Http;
using SaveNews.Handler.CreateSaveNews;
using SaveNews.Handler.GetSavedNews;
using SaveNews.Handler.DeleteSaveNews;
using SaveNews.Models;

public class DeleteSaveNewsModule : CarterModule
{
    public override void AddRoutes(IEndpointRouteBuilder app)
    {
        var saveNewsGroup = app.MapGroup("/save-news")
                               .RequireAuthorization();


        // ✅ DELETE - Remove a saved news item
        saveNewsGroup.MapDelete("{id:int}", async (int id, HttpContext context, IMediator mediator) =>
        {
            var userIdClaim = context.User.Claims.FirstOrDefault(c => c.Type == "user_id");
            if (userIdClaim == null || !int.TryParse(userIdClaim.Value, out var userId))
                return Results.Unauthorized();

            var command = new DeleteSaveNewsCommand(id, userId);
            var success = await mediator.Send(command);

            return success ? Results.NoContent() : Results.NotFound();
        });
    }
}

