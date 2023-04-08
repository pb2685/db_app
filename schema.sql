create table Transport (
	Transport_ID integer primary key,
	Shipping_Date_Time timestamp,
	Delivery_Date_Time timestamp
	);

create table Address (
	Location_Name varchar(128),
	Zipcode integer,
	City varchar(128),
	primary key (Location_Name, Zipcode)
	);
	
create table Customer(
	SSN integer primary key,
	C_Name varchar(64),
	C_Address varchar(128)
	);
	
create table CSM_Order (
	Order_ID integer primary key,
	Product varchar(128) ,
	Weight integer ,
	Source_Zipcode integer,
	Destination_Zipcode integer,
	Sender_SSN integer not null,
	Reciver_SSN integer not null,
	foreign key (Sender_SSN) references Customer(SSN),
	foreign key (Reciver_SSN) references Customer(SSN)
	);
	
create table Order_Address(
	Order_ID integer,
	Location_Name varchar(128),
	Zipcode integer,
	primary key (Order_ID, Location_Name, Zipcode), 
	foreign key (Order_ID) references CSM_Order(Order_ID),
	foreign key (Location_Name, Zipcode) references Address(Location_Name, Zipcode)
	);

create table Carrier(
	Carrier_Code varchar(32) primary key,
	Carrier_Name varchar(128)
	);

create table Vehicle (
	Vehicle_ID integer primary key,
	Source_Zipcode integer,
	Destination_Zipcode integer,
	Capacity integer,
	Since integer,
	Carrier_Code varchar(32) not null,
	foreign key (Carrier_Code) references Carrier (Carrier_Code)
	);


create table Shipping(
	Order_ID integer,
	Vehicle_ID integer,
	Transport_ID integer,
	primary key (Order_ID, Vehicle_ID, Transport_ID),
	foreign key (Order_ID) references CSM_Order(Order_ID),
	foreign key (Vehicle_ID) references Vehicle(Vehicle_ID),
	foreign key (Transport_ID) references Transport(Transport_ID)
	);



create table Order_Status (
	Order_ID integer,
	Status varchar(32),
	Time timestamp,
	primary key (Order_ID,Status),
	foreign key (Order_ID) references CSM_Order(Order_ID)
		on delete cascade
	);


create table Feedback (
	Feedback_ID integer primary key,
	Description varchar(256),
	Rating integer,
	Order_ID integer,
	foreign key (Order_ID) references CSM_Order (Order_ID)
	);
	
create table Order_Payment(
	Order_ID integer,
	Payment_ID integer,
	Date_Time timestamp,
	Amount decimal,
	primary key (Order_ID,Payment_ID),
	foreign key (Order_ID) references CSM_Order(Order_ID)
		on delete cascade
	);

create table Feedback_Customer(
	Feedback_ID integer,
	SSN integer,
	primary key (Feedback_ID, SSN),
	foreign key (Feedback_ID) references Feedback (Feedback_ID),
	foreign key (SSN) references Customer (SSN)
	);
