using Raftaar.DataLayer;
using System;

namespace ConsoleRaftaar
{
    internal class Program
    {
        static void Main(string[] args)
        {
            using (var db = new RaftaarModel())
            {
                //db.Database.Delete();

                Console.WriteLine("Welcome to Raftaar!\nRaftaar helps you manage your vehicles.");

                var vehicle = new Vehicle
                {
                    Make = "Toyota",
                    Model = "Prius",
                    Name = "Raftaar",
                    Odometer = 73000,
                    Year = 2016
                };
                db.Vehicles.Add(vehicle);

                var gas1 = new Fuel
                {
                    Odometer = 73374,
                    Date = DateTime.Parse("04/05/22"),
                    Gallons = 7.421,
                    Price = 40.51M
                };
                var gas2 = new Fuel
                {
                    Odometer = 73012,
                    Date = DateTime.Parse("04/03/22"),
                    Gallons = 4.261,
                    Price = 23.01M
                };
                db.Fuels.Add(gas1);
                db.Fuels.Add(gas2);

                var gasStation = new GasStation
                {
                    City = "Camarillo",
                    Name = "Chevron"
                };
                db.GasStations.Add(gasStation);
                db.SaveChanges();
            }
            Console.ReadKey();
        }
    }
}
