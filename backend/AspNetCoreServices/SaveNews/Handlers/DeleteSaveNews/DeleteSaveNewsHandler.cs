using MediatR;
using Microsoft.EntityFrameworkCore;
using SaveNews.Data;

namespace SaveNews.Handler.DeleteSaveNews;

// Request to delete a saved news item
public record DeleteSaveNewsCommand(int Id, int UserId) : IRequest<bool>;


public class DeleteSaveNewsCommandHandler : IRequestHandler<DeleteSaveNewsCommand, bool>
{
    private readonly AppDbContext _db;

    public DeleteSaveNewsCommandHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<bool> Handle(DeleteSaveNewsCommand request, CancellationToken cancellationToken)
    {
        // Find the saved news by ID and UserId to ensure ownership
        var saveNewsItem = await _db.SaveNews
            .FirstOrDefaultAsync(n => n.Id == request.Id && n.UserId == request.UserId, cancellationToken);

        if (saveNewsItem == null)
        {
            // Either doesn't exist OR not owned by this user
            return false;
        }

        _db.SaveNews.Remove(saveNewsItem);
        await _db.SaveChangesAsync(cancellationToken);

        return true;
    }
}
