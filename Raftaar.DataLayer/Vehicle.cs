using System.ComponentModel.DataAnnotations;

namespace Raftaar.DataLayer
{
    public class Vehicle
    {
        [Key]
        public int Id { get; set; }
        public string Name { get; set; }
        public string Make { get; set; }
        public string Model { get; set; }
        public int Year { get; set; }
        public int Odometer { get; set; }

        #region Methods
        public override string ToString() => $"Id:{Id}, Name:{Name}, Make:{Make}, Model:{Model}, Year:{Year}, Odometer:{Odometer}";
        #endregion
    }
}
