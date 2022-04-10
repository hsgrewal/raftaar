namespace Raftaar.DataLayer
{
    public class GasStation
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string City { get; set; }

        #region Methods
        public override string ToString() => $"Id:{Id}, Name:{Name}, City:{City}";
        #endregion
    }
}
