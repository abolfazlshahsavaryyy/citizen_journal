namespace SaveNews.Models;
public class SaveNewsModel
{
    public int Id {get;set;}
    public int UserId {get;set;}
    public int NewsId {get;set;}
    public DateTime CreateAt {get;set;}
    public string TextContent{get;set;}
}