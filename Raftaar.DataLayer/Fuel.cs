using System;

namespace Raftaar.DataLayer
{
    public class Fuel
    {
        public int Id { get; set; }
        public DateTime Date { get; set; }
        public double Gallons { get; set; }
        public decimal Price { get; set; }
        public int Odometer { get; set; }

        public int VehicleId { get; set; }
        public virtual Vehicle Vehicle { get; set; }

        public int GasStationId { get; set; }
        public virtual GasStation GasStation { get; set; }
    }
}
