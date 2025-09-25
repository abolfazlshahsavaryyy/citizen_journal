using System;

namespace ShareNewsGrpc.Models
{
    public class ShareNews
    {
        public int Id { get; set; } // Primary Key
        public int UserIdSender { get; set; }
        public int NewsId { get; set; }
        public int UserIdReceiver { get; set; }
        public string Content { get; set; }
        public DateTime CreatedAt { get; set; }

    }
}
