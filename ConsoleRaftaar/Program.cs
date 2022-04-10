using Raftaar.DataLayer;
using System;

namespace ConsoleRaftaar
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Welcome to Raftaar!\nRaftaar helps you manage your vehicles.");

            // Create vehicle
            var vehicle = new Vehicle
            {
                Make = "Toyota",
                Model = "Prius",
                Name = "Raftaar",
                Odometer = 73000,
                Year = 2016
            };
            Console.WriteLine($"Created vehicle: [{vehicle}]");

            Console.WriteLine($"Saving vehicle [{vehicle}] to DB");
            // Save vehicle to db
            using (var db = new RaftaarModel())
            {
                db.Vehicles.Add(vehicle);
                db.SaveChanges();
            }
            Console.WriteLine($"Saved vehicle [{vehicle}] to DB");

            // Create default Gas Station
            var gasStation = new GasStation
            {
                Name = "DEFAULT",
                Description = "Default Gas Station"
            };
            Console.WriteLine($"Created default gas station: [{gasStation}]");

            Console.WriteLine($"Saving default gas station [{gasStation}] to DB");
            // Save gas station to db
            using (var db = new RaftaarModel())
            {
                db.GasStations.Add(gasStation);
                db.SaveChanges();
            }
            Console.WriteLine($"Saved default gas station [{gasStation}] to DB");

            // Create gas transactions
            var gas1 = new Fuel
            {
                Odometer = 73374,
                Date = DateTime.Parse("04/05/22"),
                Gallons = 7.421,
                Price = 40.51M,
                GasStationId = 1,
                VehicleId = 1
            };
            var gas2 = new Fuel
            {
                Odometer = 73012,
                Date = DateTime.Parse("04/03/22"),
                Gallons = 4.261,
                Price = 23.01M,
                GasStationId = 1,
                VehicleId = 1
            };
            Console.WriteLine($"Created gas transactions: [{gas1}] & [{gas2}]");

            Console.WriteLine($"Saving gas transactions: [{gas1}] & [{gas2}] to DB");
            // Save gas transactions to db separately
            using (var db = new RaftaarModel())
            {
                db.Fuels.Add(gas1);
                db.SaveChanges();
            }
            using (var db = new RaftaarModel())
            {
                db.Fuels.Add(gas2);
                db.SaveChanges();
            }
            Console.WriteLine($"Saved gas transactions: [{gas1}] & [{gas2}] to DB");

            // Create Gas Station
            var gasStation1 = new GasStation
            {
                City = "Camarillo",
                Name = "Chevron"
            };
            Console.WriteLine($"Created gas station: [{gasStation1}]");

            Console.WriteLine($"Saving gas station [{gasStation1}] to DB");
            // Save gas station to db
            using (var db = new RaftaarModel())
            {
                db.GasStations.Add(gasStation1);
                db.SaveChanges();
            }
            Console.WriteLine($"Saved gas station [{gasStation1}] to DB");

            Console.WriteLine("Enter any key to exit...");
            Console.ReadLine();
        }
    }
}
