using MediatR;
using SaveNews.Models;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using SaveNews.Data;


namespace SaveNews.Handler.GetSavedNews;

public record GetSavedNewsQuery(int UserId) : IRequest<List<SaveNewsModel>>;




public class GetSavedNewsQueryHandler : IRequestHandler<GetSavedNewsQuery, List<SaveNewsModel>>
{
    private readonly AppDbContext _db;

    public GetSavedNewsQueryHandler(AppDbContext db)
    {
        _db = db;
    }

    public async Task<List<SaveNewsModel>> Handle(GetSavedNewsQuery request, CancellationToken cancellationToken)
    {
        return await _db.SaveNews
            .Where(n => n.UserId == request.UserId)
            .OrderByDescending(n => n.CreateAt)
            .ToListAsync(cancellationToken);
    }
}
