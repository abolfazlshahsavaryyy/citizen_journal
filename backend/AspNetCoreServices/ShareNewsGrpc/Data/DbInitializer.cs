using System;
using System.Linq;
using ShareNewsGrpc.Data;
using ShareNewsGrpc.Models;

public static class DbInitializer
{
    public static void Seed(AppDbContext context)
    {
        if (context.ShareNews.Any()) return; // Already seeded

        context.ShareNews.AddRange(
            new ShareNews
            {
                UserIdSender = 1,
                NewsId = 1,
                UserIdReceiver = 2,
                Content = "Breaking news from User 1 to User 2",
                CreatedAt = DateTime.UtcNow
            },
            new ShareNews
            {
                UserIdSender = 2,
                NewsId = 2,
                UserIdReceiver = 3,
                Content = "Second message seeded into DB",
                CreatedAt = DateTime.UtcNow
            }
        );

        context.SaveChanges();
    }
}
