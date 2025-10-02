using MediatR;
using SaveNews.Models;
using SaveNews.Data;
namespace SaveNews.Handler.CreateSaveNews;
public record SaveNewsCommand(int NewsId, string TextContent, int UserId) : IRequest<SaveNewsModel>;



public class SaveNewsCommandHandler : IRequestHandler<SaveNewsCommand, SaveNewsModel>
{
    private readonly AppDbContext _db;

    public SaveNewsCommandHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<SaveNewsModel> Handle(SaveNewsCommand request, CancellationToken cancellationToken)
    {
        var model = new SaveNewsModel
        {
            UserId = request.UserId,
            NewsId = request.NewsId,
            TextContent = request.TextContent,
            CreateAt = DateTime.UtcNow
        };

        _db.SaveNews.Add(model);
        await _db.SaveChangesAsync(cancellationToken);

        return model;
    }
}
