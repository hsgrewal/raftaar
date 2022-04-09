using System;
using System.Data.Entity;
using System.Linq;

namespace Raftaar.DataLayer
{
    public class RaftaarModel : DbContext
    {
        // Your context has been configured to use a 'RaftaarModel' connection string from your application's 
        // configuration file (App.config or Web.config). By default, this connection string targets the 
        // 'Raftaar.DataLayer.RaftaarModel' database on your LocalDb instance. 
        // 
        // If you wish to target a different database and/or database provider, modify the 'RaftaarModel' 
        // connection string in the application configuration file.
        public RaftaarModel() : base("name=RaftaarModel") { }

        // Add a DbSet for each entity type that you want to include in your model. For more information 
        // on configuring and using a Code First model, see http://go.microsoft.com/fwlink/?LinkId=390109.

        // public virtual DbSet<MyEntity> MyEntities { get; set; }
        public virtual DbSet<Vehicle> Vehicles { get; set; }
        public virtual DbSet<Fuel> Fuels { get; set; }
        public virtual DbSet<GasStation> GasStations { get; set; }
    }
}