using Microsoft.EntityFrameworkCore;
using ShareNewsGrpc.Models;

namespace ShareNewsGrpc.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<ShareNews> ShareNews { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<ShareNews>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.UserIdReceiver).IsRequired();
                entity.Property(e => e.UserIdSender).IsRequired();
                entity.Property(e => e.Content).IsRequired();
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("GETDATE()");
            });
        }
    }
}
