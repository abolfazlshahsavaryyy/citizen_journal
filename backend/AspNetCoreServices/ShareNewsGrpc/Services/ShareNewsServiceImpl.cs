using Grpc.Core;
using ShareNewsGrpc.Models;
using ShareNewsGrpc.Protos;
using Microsoft.EntityFrameworkCore;
using ShareNewsGrpc.Data;

public class ShareNewsServiceImpl : ShareNewsService.ShareNewsServiceBase
{
    private readonly AppDbContext _context;

    public ShareNewsServiceImpl(AppDbContext context)
    {
        _context = context;
    }


    public override async Task<GetShareNewsByUserResponse> GetShareNewsByUser(
    GetShareNewsByUserRequest request,
    ServerCallContext context)
    {
        var items = await _context.ShareNews
            .Where(sn => sn.UserIdSender == request.UserId || sn.UserIdReceiver == request.UserId)
            .ToListAsync();

        var response = new GetShareNewsByUserResponse();
        response.Items.AddRange(items.Select(sn => new ShareNewsMessage
        {
            Id = sn.Id,
            UserIdSender = sn.UserIdSender,
            NewsId = sn.NewsId,
            UserIdReceiver = sn.UserIdReceiver,
            Content = sn.Content,
            CreatedAt = sn.CreatedAt.ToString("O")
        }));

        return response;
    }
    public override async Task<AddShareNewsResponse> AddShareNews(
    AddShareNewsRequest request,
    ServerCallContext context)
    {
        var entity = new ShareNews
        {
            UserIdSender = request.UserIdSender,
            NewsId = request.NewsId,
            UserIdReceiver = request.UserIdReceiver,
            Content = request.Content,
            CreatedAt = DateTime.UtcNow
        };

        _context.ShareNews.Add(entity);
        await _context.SaveChangesAsync();

        return new AddShareNewsResponse
        {
            Item = new ShareNewsMessage
            {
                Id = entity.Id,
                UserIdSender = entity.UserIdSender,
                NewsId = entity.NewsId,
                UserIdReceiver = entity.UserIdReceiver,
                Content = entity.Content,
                CreatedAt = entity.CreatedAt.ToString("O")
            }
        };
    }
    public override async Task<RemoveShareNewsResponse> RemoveShareNews(
    RemoveShareNewsRequest request,
    ServerCallContext context
)
{
    // Step 1: Find the entity by Id
    var entity = await _context.ShareNews.FindAsync(request.ShareNewsId);

    if (entity == null)
    {
        // Optional: Throw a gRPC RpcException if not found
        throw new RpcException(new Status(StatusCode.NotFound, $"ShareNews with Id={request.ShareNewsId} not found"));
    }

    // Step 2: Remove the entity
    _context.ShareNews.Remove(entity);

    // Step 3: Save changes to the database
    await _context.SaveChangesAsync();

    // Step 4: Return response with removed Id
    return new RemoveShareNewsResponse
    {
        ShareNewsId = request.ShareNewsId
    };
}




}
