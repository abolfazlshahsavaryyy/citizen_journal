namespace SaveNews.Data;

using Microsoft.EntityFrameworkCore;
using SaveNews.Models;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<SaveNewsModel> SaveNews { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<SaveNewsModel>(entity =>
        {
            entity.HasKey(e => e.Id);

            entity.Property(e => e.UserId)
                  .IsRequired();

            entity.Property(e => e.NewsId)
                  .IsRequired();

            entity.Property(e => e.CreateAt)
                  .IsRequired();

            entity.Property(e => e.TextContent)
                  .HasMaxLength(20)
                  .IsRequired();

            entity.ToTable("SaveNews");
        });
    }
}
