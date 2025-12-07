DROP DATABASE IF EXISTS `husky-fix`;
CREATE DATABASE `husky-fix`;
USE `husky-fix`;

DROP TABLE IF EXISTS employee;
CREATE TABLE employee
(
    employeeID   INT PRIMARY KEY,
    firstName    VARCHAR(50),
    lastName     VARCHAR(50),
    employeeType VARCHAR(50),
    email        VARCHAR(50) UNIQUE NOT NULL,
    salary       INT
);

DROP TABLE IF EXISTS student;
CREATE TABLE student
(                             -- renter profile
    studentID   INT PRIMARY KEY,
    firstName   VARCHAR(50),
    lastName    VARCHAR(50),
    email       VARCHAR(100), -- Considering UNIQUE NOT NULL
    paymentInfo VARCHAR(19)   -- Not sure what this is, but seems like composite of credit card num and cvv
);

DROP TABLE IF EXISTS building;
CREATE TABLE building
(
    buildingID INT PRIMARY KEY,
    address    VARCHAR(100),
    managerID  INT NOT NULL,
    FOREIGN KEY (managerID) REFERENCES employee (employeeID)
);

-- Assumption: students can only rent one apartment --
DROP TABLE IF EXISTS apartment;
CREATE TABLE apartment
(
    buildingID INT,
    aptNumber  INT,  -- This is a better name then roomNumber imo
    rentalCost INT,  -- considering NOT NLL
    dateRented DATE, -- NULL if vacant
    renterId   INT,  -- NULL if vacant
    PRIMARY KEY (buildingId, aptNumber),
    FOREIGN KEY (buildingID) REFERENCES building (buildingID),
    FOREIGN KEY (renterId) REFERENCES student (studentID)
);


DROP TABLE IF EXISTS maintenanceRequest;
CREATE TABLE maintenanceRequest
(
    requestID           INT PRIMARY KEY,
    studentRequestingID INT,           -- considering NOT NULL (does every request need to be from a student?)
    buildingID          INT NOT NULL,
    aptNumber           INT NOT NULL,
    issueType           VARCHAR(50),
    issueDescription    TINYTEXT,
    activeStatus        VARCHAR(50),   -- "En route", "In progress", "Blocked", "Completed"
    dateRequested       DATE,
    dateCompleted       DATE,

    priority            INT DEFAULT 0, -- higher = more urgent
    scheduledDate       DATE,          -- day the job is scheduled
    issuePhotos         TEXT,          -- using text to reference path to photo? Idk what to put here
    completionNotes     TINYTEXT,

    FOREIGN KEY (studentRequestingID) REFERENCES student (studentID),
    FOREIGN KEY (buildingID, aptNumber) REFERENCES apartment (buildingID, aptNumber)
);

DROP TABLE IF EXISTS tool;
CREATE TABLE tool
(
    toolID   INT PRIMARY KEY,
    name     VARCHAR(50),
    quantity INT NOT NULL
);


DROP TABLE IF EXISTS part;
CREATE TABLE part
(
    partID   INT PRIMARY KEY,
    name     VARCHAR(50),
    cost     INT NOT NULL, -- prob should be cost in cents to avoid float rounding errors
    quantity INT NOT NULL
);

-- Bridge Tables --
DROP TABLE IF EXISTS partUsed;
CREATE TABLE partUsed
(
    partID    INT,
    requestID INT,
    PRIMARY KEY (partID, requestID),
    FOREIGN KEY (partID) REFERENCES part (partID),
    FOREIGN KEY (requestID) REFERENCES maintenanceRequest (requestID)
);

DROP TABLE IF EXISTS toolUsed;
CREATE TABLE toolUsed
(
    toolID    INT,
    requestID INT,
    PRIMARY KEY (toolID, requestID),
    FOREIGN KEY (toolID) REFERENCES tool (toolID),
    FOREIGN KEY (requestID) REFERENCES maintenanceRequest (requestID)
);

DROP TABLE IF EXISTS employeeAssigned;
CREATE TABLE employeeAssigned
(
    employeeID INT,
    requestID  INT,
    PRIMARY KEY (employeeID, requestID),
    FOREIGN KEY (employeeID) REFERENCES employee (employeeID),
    FOREIGN KEY (requestID) REFERENCES maintenanceRequest (requestID)
);

insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (1, 'Lorelle', 'Glisenan', 'Mechanic', 'lglisenan0@elpais.com', 120688);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (2, 'Lennard', 'Lowerson', 'Carpenter', 'llowerson1@yolasite.com', 237636);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (3, 'Yehudit', 'Ayto', 'Plumber', 'yayto2@irs.gov', 241978);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (4, 'Bellina', 'Danielczyk', 'Mechanic', 'bdanielczyk3@businessweek.com', 249514);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (5, 'Roderic', 'Gyurko', 'Carpenter', 'rgyurko4@flickr.com', 37872);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (6, 'Karry', 'Foulsham', 'Security', 'kfoulsham5@trellian.com', 69564);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (7, 'Rakel', 'Bugby', 'Plumber', 'rbugby6@umn.edu', 84936);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (8, 'Rafaelia', 'Phin', 'Carpenter', 'rphin7@pen.io', 105785);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (9, 'Sadie', 'Dugue', 'Landlord', 'sdugue8@mediafire.com', 129349);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (10, 'Rosemarie', 'Matresse', 'Landlord', 'rmatresse9@networkadvertising.org', 98446);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (11, 'Janek', 'Rany', 'Landlord', 'jranya@arizona.edu', 194152);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (12, 'Tammi', 'Honeyghan', 'Carpenter', 'thoneyghanb@amazon.de', 208416);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (13, 'Dyanna', 'D''Abbot-Doyle', 'Plumber', 'ddabbotdoylec@marketwatch.com', 30521);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (14, 'Ninnette', 'Betterton', 'Security', 'nbettertond@ucoz.com', 40896);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (15, 'Georgeanna', 'Threadgall', 'Security', 'gthreadgalle@hatena.ne.jp', 195407);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (16, 'Geri', 'Andreone', 'Resident Assistant', 'gandreonef@chron.com', 61694);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (17, 'Nananne', 'Cridland', 'Electrician', 'ncridlandg@unc.edu', 218038);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (18, 'Derrek', 'Mattin', 'Resident Assistant', 'dmattinh@businessweek.com', 78518);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (19, 'Jany', 'Grigaut', 'Security', 'jgrigauti@wikimedia.org', 47453);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (20, 'Maure', 'Semonin', 'Security', 'msemoninj@about.me', 60870);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (21, 'Culley', 'Du Pre', 'Mechanic', 'cduprek@europa.eu', 68515);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (22, 'Petra', 'Pershouse', 'Security', 'ppershousel@prnewswire.com', 231493);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (23, 'Gert', 'Reignould', 'Electrician', 'greignouldm@squidoo.com', 178342);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (24, 'Burgess', 'Ballintime', 'Landlord', 'bballintimen@wikimedia.org', 181055);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (25, 'Aida', 'Giacovelli', 'Electrician', 'agiacovellio@youtube.com', 173226);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (26, 'Nerta', 'Paschke', 'Resident Assistant', 'npaschkep@oracle.com', 204370);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (27, 'Dannye', 'Quaintance', 'Electrician', 'dquaintanceq@xrea.com', 236993);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (28, 'Ame', 'Hamly', 'Electrician', 'ahamlyr@cnn.com', 197883);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (29, 'Cleo', 'Spargo', 'Plumber', 'cspargos@example.com', 111932);
insert into employee (employeeID, firstName, lastName, employeeType, email, salary) values (30, 'Gun', 'Fosse', 'Plumber', 'gfosset@narod.ru', 245144);


insert into student (studentID, firstName, lastName, email, paymentInfo) values (1, 'Felic', 'Abbis', 'fabbis0@storify.com', '6763368775315408815');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (2, 'Darcey', 'Tregunnah', 'dtregunnah1@wsj.com', '3580750711286908');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (3, 'Terrye', 'Laroze', 'tlaroze2@zimbio.com', '372301724790102');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (4, 'Ozzie', 'Brewers', 'obrewers3@wp.com', '3528767275890227');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (5, 'Antoine', 'Weldrake', 'aweldrake4@wp.com', '5002357859022411');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (6, 'Wynnie', 'Fidgin', 'wfidgin5@t-online.de', '3536009271629972');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (7, 'Sly', 'Kamall', 'skamall6@pcworld.com', '3566694445112063');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (8, 'Merola', 'Hartigan', 'mhartigan7@nymag.com', '6767562607865226');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (9, 'Athena', 'Matzaitis', 'amatzaitis8@php.net', '3570028960942337');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (10, 'Natasha', 'McNea', 'nmcnea9@vimeo.com', '4936311482145292772');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (11, 'Tadio', 'Windus', 'twindusa@usatoday.com', '3588492938339754');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (12, 'Charis', 'Campany', 'ccampanyb@sohu.com', '3534686369952762');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (13, 'Val', 'Drissell', 'vdrissellc@telegraph.co.uk', '56022382922836760');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (14, 'Freddie', 'McGettigan', 'fmcgettigand@washington.edu', '6334261926412907104');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (15, 'Tull', 'McNelly', 'tmcnellye@sogou.com', '4405396934155685');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (16, 'Rania', 'Verissimo', 'rverissimof@ameblo.jp', '201820893400299');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (17, 'Sol', 'Dorie', 'sdorieg@china.com.cn', '3580098420371698');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (18, 'Barnard', 'Coolican', 'bcoolicanh@joomla.org', '5602245548245135');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (19, 'Althea', 'Pigott', 'apigotti@ox.ac.uk', '633349937652720195');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (20, 'Estele', 'Kiddell', 'ekiddellj@soundcloud.com', '36481611573288');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (21, 'Derron', 'Frammingham', 'dframminghamk@simplemachines.org', '3578618287844950');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (22, 'Vin', 'Fawthorpe', 'vfawthorpel@bluehost.com', '5010121709668868');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (23, 'Gonzales', 'Ebsworth', 'gebsworthm@istockphoto.com', '3534495233737239');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (24, 'Nadine', 'Bertl', 'nbertln@omniture.com', '3539905211762590');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (25, 'Jo', 'Jiroutka', 'jjiroutkao@si.edu', '6388563120612730');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (26, 'Karyn', 'Pilgram', 'kpilgramp@tinypic.com', '670602196010126983');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (27, 'Orin', 'Keunemann', 'okeunemannq@dyndns.org', '3567898596932737');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (28, 'Bjorn', 'Balshaw', 'bbalshawr@cnn.com', '3550183951194465');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (29, 'Demetra', 'Liffe', 'dliffes@unc.edu', '6388818323828073');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (30, 'Jim', 'Northedge', 'jnorthedget@unicef.org', '4041594584660141');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (31, 'Sigvard', 'Hullbrook', 'shullbrooku@adobe.com', '3558753878158678');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (32, 'Petronille', 'Matussow', 'pmatussowv@java.com', '6377097352566507');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (33, 'Connie', 'Sanham', 'csanhamw@rambler.ru', '3583096833427377');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (34, 'Milo', 'Palumbo', 'mpalumbox@foxnews.com', '3580332533101258');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (35, 'Mikkel', 'Sutherel', 'msutherely@freewebs.com', '3572622173141519');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (36, 'Hildagarde', 'Lowdeane', 'hlowdeanez@vkontakte.ru', '5602215343179193');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (37, 'Daphna', 'Tynnan', 'dtynnan10@sourceforge.net', '3586096215161419');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (38, 'Imogene', 'Timmermann', 'itimmermann11@nih.gov', '3562728571090075');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (39, 'Parnell', 'Filippone', 'pfilippone12@myspace.com', '5536411436674411');
insert into student (studentID, firstName, lastName, email, paymentInfo) values (40, 'Humbert', 'Earnshaw', 'hearnshaw13@usnews.com', '3576858623083135');


insert into building (buildingID, address, managerID) values (1, '3 Bonner Trail', 15);
insert into building (buildingID, address, managerID) values (2, '92 Nelson Alley', 11);
insert into building (buildingID, address, managerID) values (3, '0725 Mcguire Alley', 29);
insert into building (buildingID, address, managerID) values (4, '46 Golf Way', 16);
insert into building (buildingID, address, managerID) values (5, '77 Welch Road', 14);
insert into building (buildingID, address, managerID) values (6, '4 Bellgrove Street', 8);
insert into building (buildingID, address, managerID) values (7, '62176 Debs Pass', 1);
insert into building (buildingID, address, managerID) values (8, '37 Lighthouse Bay Terrace', 3);
insert into building (buildingID, address, managerID) values (9, '938 Montana Terrace', 28);
insert into building (buildingID, address, managerID) values (10, '70863 Mitchell Alley', 12);


insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (1, 1, 2449, '2025-05-20 19:54:22', 35);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (1, 2, 2000, NULL, NULL);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (1, 3, 1488, '2025-01-10 08:12:50', 23);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (1, 4, 1126, '2025-01-09 09:15:48', 29);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (1, 5, 1479, '2025-05-01 05:24:14', 16);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (2, 1, 2223, '2025-05-31 18:02:40', 18);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (2, 2, 2849, NULL, NULL);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (2, 3, 2238, '2025-05-31 20:57:09', 26);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (2, 4, 1326, '2025-08-24 05:19:14', 32);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (2, 5, 1029, '2025-11-05 19:27:03', 20);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (3, 1, 1632, '2025-06-02 15:23:47', 11);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (3, 2, 2491, '2025-06-09 16:58:43', 30);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (3, 3, 2311, '2025-04-23 01:39:14', 27);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (3, 4, 1040, '2025-02-22 00:13:53', 19);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (3, 5, 2241, '2025-07-25 13:41:37', 2);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (4, 1, 2907, '2025-11-21 02:04:48', 34);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (4, 2, 1579, '2025-07-24 15:27:39', 36);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (4, 3, 2515, '2025-11-21 15:12:57', 36);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (4, 4, 1724, '2024-12-26 12:36:58', 22);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (4, 5, 2271, NULL, NULL);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (5, 1, 1755, '2025-08-04 20:57:41', 24);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (5, 2, 1059, '2025-12-03 22:22:23', 23);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (5, 3, 1907, '2025-10-07 10:46:10', 24);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (5, 4, 1281, '2025-07-27 01:26:26', 12);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (5, 5, 2153, '2025-03-19 08:02:22', 8);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (6, 1, 2339, '2025-11-19 09:09:19', 17);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (6, 2, 2662, '2025-02-07 09:27:35', 14);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (6, 3, 1766, '2024-12-10 03:06:50', 15);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (6, 4, 2837, '2025-02-18 15:22:23', 7);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (6, 5, 2837, '2025-07-06 06:26:01', 25);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (7, 1, 1004, NULL, NULL);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (7, 2, 2567, '2025-04-23 04:48:06', 10);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (7, 3, 2961, '2025-10-20 00:35:22', 17);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (7, 4, 2081, '2025-04-01 23:34:59', 1);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (7, 5, 1660, '2025-04-12 13:13:14', 11);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (8, 1, 2865, '2025-12-02 17:34:02', 13);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (8, 2, 1040, '2025-04-28 21:13:23', 13);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (8, 3, 1850, '2025-02-06 04:59:46', 18);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (8, 4, 1647, '2025-05-20 04:46:39', 12);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (8, 5, 2292, '2025-08-05 17:20:09', 34);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (9, 1, 1629, '2025-06-17 10:44:55', 32);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (9, 2, 1377, '2025-06-03 19:25:44', 34);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (9, 3, 1477, '2025-07-14 22:22:46', 28);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (9, 4, 2327, NULL, NULL);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (9, 5, 2484, NULL, NULL);

insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (10, 1, 1280, '2025-01-13 01:39:58', 6);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (10, 2, 1134, '2025-03-02 21:26:55', 12);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (10, 3, 2704, NULL, NULL);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (10, 4, 1277, '2025-07-04 05:08:46', 10);
insert into apartment (buildingID, aptNumber, rentalCost, dateRented, renterID) values (10, 5, 1177, '2025-02-15 08:28:52', 6);


insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (1, 5, 2, 1, 'Plumbing', 'lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien', 'Completed', '2025-05-21 09:10:49', '2025-07-31 17:48:24', 3, '2025-06-02 13:25:58', 'http://dummyimage.com/229x100.png/5fa2dd/ffffff', 'donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (2, 7, 10, 4, 'Electrical', 'non mi integer ac neque duis bibendum morbi non quam nec dui luctus rutrum nulla tellus in sagittis', 'Blocked', '2025-11-27 07:12:17', NULL, 0, '2024-12-19 03:21:46', 'http://dummyimage.com/222x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (3, 8, 10, 2, 'Structural', 'ipsum dolor sit amet consectetuer adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut', 'Completed', '2025-09-21 04:57:37', '2025-08-02 20:09:55', 1, '2025-05-19 22:52:39', 'http://dummyimage.com/193x100.png/5fa2dd/ffffff', 'orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (4, 16, 9, 1, 'Electrical', 'ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam pretium iaculis', 'In progress', '2025-05-22 09:48:42', NULL, 3, '2025-10-12 18:53:28', 'http://dummyimage.com/163x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (5, 8, 3, 2, 'Structural', 'donec odio justo sollicitudin ut suscipit a feugiat et eros vestibulum ac est', 'Blocked', '2025-08-19 18:36:21', NULL, 1, '2025-02-08 18:46:17', 'http://dummyimage.com/134x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (6, 15, 9, 4, 'Structural', 'dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus', 'Completed', '2025-01-23 03:08:34', '2025-01-11 11:56:57', 4, '2025-07-02 13:26:36', 'http://dummyimage.com/170x100.png/ff4444/ffffff', 'donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (7, 23, 3, 5, 'Other', 'vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan', 'In progress', '2025-03-10 09:39:56', NULL, 4, '2025-02-27 16:24:42', 'http://dummyimage.com/126x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (8, 25, 8, 3, 'Structural', 'a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla', 'En Route', '2025-08-23 03:23:31', NULL, 3, '2025-07-05 16:42:13', 'http://dummyimage.com/215x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (9, 30, 4, 2, 'Plumbing', 'consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel', 'En Route', '2025-10-18 20:34:58', NULL, 1, '2025-08-26 05:38:14', 'http://dummyimage.com/182x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (10, 39, 3, 5, 'Other', 'metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc donec quis orci eget', 'Completed', '2025-01-05 06:54:19', '2025-09-06 09:20:54', 0, '2025-02-13 02:03:34', 'http://dummyimage.com/172x100.png/cc0000/ffffff', 'donec vitae nisi nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (11, 26, 4, 2, 'Other', 'donec dapibus duis at velit eu est congue elementum in hac habitasse', 'Blocked', '2025-04-10 22:28:53', NULL, 4, '2025-01-19 20:46:24', 'http://dummyimage.com/243x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (12, 8, 4, 5, 'Other', 'aliquet pulvinar sed nisl nunc rhoncus dui vel sem sed sagittis nam congue risus semper porta volutpat quam', 'In progress', '2025-02-08 01:37:16', NULL, 1, '2025-09-13 15:17:09', 'http://dummyimage.com/218x100.png/dddddd/000000', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (13, 25, 5, 4, 'Plumbing', 'morbi non lectus aliquam sit amet diam in magna bibendum', 'Completed', '2025-06-28 00:51:14', '2025-11-23 14:00:15', 0, '2025-03-02 22:06:33', 'http://dummyimage.com/206x100.png/dddddd/000000', 'donec ut mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (14, 19, 6, 4, 'Other', 'nisl venenatis lacinia aenean sit amet justo morbi ut odio cras mi pede malesuada in imperdiet', 'En Route', '2025-11-15 01:39:59', NULL, 1, '2025-05-04 01:09:07', 'http://dummyimage.com/171x100.png/dddddd/000000', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (15, 32, 2, 5, 'Structural', 'tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu', 'In progress', '2025-01-03 11:27:14', NULL, 4, '2025-11-25 17:00:42', 'http://dummyimage.com/208x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (16, 28, 3, 2, 'Electrical', 'condimentum curabitur in libero ut massa volutpat convallis morbi odio odio elementum eu interdum eu tincidunt', 'Blocked', '2025-06-25 23:35:05', NULL, 4, '2025-08-07 10:41:47', 'http://dummyimage.com/147x100.png/dddddd/000000', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (17, 30, 10, 3, 'Other', 'facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus', 'En Route', '2025-02-07 09:28:32', NULL, 3, '2025-08-25 13:33:50', 'http://dummyimage.com/108x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (18, 24, 8, 4, 'Other', 'tempus vel pede morbi porttitor lorem id ligula suspendisse ornare', 'Blocked', '2024-12-13 10:26:20', NULL, 1, '2025-09-19 06:33:57', 'http://dummyimage.com/186x100.png/dddddd/000000', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (19, 4, 6, 5, 'Other', 'diam cras pellentesque volutpat dui maecenas tristique est et tempus semper est quam pharetra magna ac consequat metus', 'En Route', '2025-01-31 12:51:25', NULL, 1, '2025-02-18 04:04:09', 'http://dummyimage.com/156x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (20, 6, 5, 4, 'Plumbing', 'amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum', 'Blocked', '2025-07-09 21:43:22', NULL, 3, '2025-02-20 13:10:59', 'http://dummyimage.com/210x100.png/dddddd/000000', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (21, 10, 4, 5, 'Electrical', 'at vulputate vitae nisl aenean lectus pellentesque eget nunc donec quis orci eget orci vehicula condimentum', 'In progress', '2025-07-19 17:26:53', NULL, 0, '2025-03-27 10:01:48', 'http://dummyimage.com/226x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (22, 39, 3, 2, 'Other', 'duis bibendum morbi non quam nec dui luctus rutrum nulla', 'In progress', '2025-02-22 08:26:12', NULL, 2, '2025-02-05 08:46:21', 'http://dummyimage.com/167x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (23, 12, 5, 1, 'Electrical', 'praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget tempus vel pede', 'En Route', '2025-09-28 01:42:39', NULL, 1, '2025-04-13 21:27:48', 'http://dummyimage.com/108x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (24, 32, 1, 3, 'Electrical', 'quisque ut erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam', 'Blocked', '2025-05-23 03:23:18', NULL, 3, '2024-12-29 08:35:30', 'http://dummyimage.com/249x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (25, 14, 6, 4, 'Plumbing', 'amet cursus id turpis integer aliquet massa id lobortis convallis tortor', 'In progress', '2025-02-25 22:02:17', NULL, 2, '2025-06-24 07:50:31', 'http://dummyimage.com/235x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (26, 14, 6, 3, 'Structural', 'vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est donec', 'Blocked', '2025-02-09 08:40:23', NULL, 4, '2025-07-01 23:27:35', 'http://dummyimage.com/140x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (27, 37, 9, 4, 'Electrical', 'justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat', 'Completed', '2025-02-12 12:35:54', '2025-07-21 20:04:20', 3, '2025-05-31 00:47:18', 'http://dummyimage.com/154x100.png/ff4444/ffffff', 'commodo vulputate justo in blandit ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (28, 24, 6, 5, 'Electrical', 'lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in', 'Blocked', '2025-09-04 03:33:02', NULL, 2, '2025-11-13 17:12:22', 'http://dummyimage.com/115x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (29, 30, 1, 2, 'Other', 'nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut', 'Completed', '2025-02-08 00:21:54', '2025-09-29 10:50:35', 5, '2025-05-15 00:36:22', 'http://dummyimage.com/226x100.png/dddddd/000000', 'in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (30, 29, 8, 4, 'Structural', 'mattis nibh ligula nec sem duis aliquam convallis nunc proin at', 'Completed', '2025-04-08 09:07:40', '2025-03-29 19:52:17', 1, '2025-10-19 15:25:52', 'http://dummyimage.com/106x100.png/dddddd/000000', 'nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue a suscipit');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (31, 21, 2, 4, 'Structural', 'fusce consequat nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis', 'Completed', '2024-12-09 23:01:03', '2025-08-14 10:48:30', 0, '2025-11-29 05:45:01', 'http://dummyimage.com/213x100.png/ff4444/ffffff', 'facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (32, 6, 7, 5, 'Electrical', 'ut blandit non interdum in ante vestibulum ante ipsum primis in faucibus', 'Completed', '2025-07-02 20:25:06', '2025-10-23 02:49:17', 3, '2025-02-03 01:48:10', 'http://dummyimage.com/220x100.png/ff4444/ffffff', 'nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede justo eu massa');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (33, 40, 1, 4, 'Electrical', 'quisque ut erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam augue quam', 'Blocked', '2025-02-19 18:11:23', NULL, 4, '2025-06-10 10:26:08', 'http://dummyimage.com/146x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (34, 27, 10, 3, 'Electrical', 'neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in', 'En Route', '2024-12-17 01:38:14', NULL, 5, '2025-11-16 08:02:13', 'http://dummyimage.com/166x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (35, 4, 7, 3, 'Structural', 'sapien varius ut blandit non interdum in ante vestibulum ante ipsum', 'En Route', '2025-09-26 16:23:47', NULL, 3, '2025-04-27 13:57:16', 'http://dummyimage.com/107x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (36, 26, 2, 5, 'Plumbing', 'massa quis augue luctus tincidunt nulla mollis molestie lorem quisque', 'In progress', '2025-11-15 14:07:38', NULL, 4, '2025-10-30 07:40:57', 'http://dummyimage.com/193x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (37, 16, 5, 4, 'Other', 'nunc proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut', 'Blocked', '2025-03-01 17:25:36', NULL, 0, '2025-10-29 04:13:10', 'http://dummyimage.com/177x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (38, 2, 2, 1, 'Structural', 'sit amet diam in magna bibendum imperdiet nullam orci pede venenatis non', 'In progress', '2025-07-29 00:14:55', NULL, 0, '2025-11-01 17:08:36', 'http://dummyimage.com/207x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (39, 37, 6, 1, 'Electrical', 'libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum', 'Completed', '2025-10-25 22:11:35', '2025-03-26 09:33:31', 4, '2025-03-16 23:21:05', 'http://dummyimage.com/218x100.png/cc0000/ffffff', 'amet turpis elementum ligula vehicula consequat morbi a ipsum integer a nibh in quis justo');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (40, 21, 3, 4, 'Structural', 'molestie sed justo pellentesque viverra pede ac diam cras pellentesque volutpat dui maecenas', 'En Route', '2025-08-26 22:55:31', NULL, 5, '2025-08-20 14:41:21', 'http://dummyimage.com/116x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (41, 22, 4, 1, 'Electrical', 'non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing', 'Blocked', '2025-01-14 17:16:20', NULL, 3, '2025-02-02 19:21:13', 'http://dummyimage.com/135x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (42, 4, 6, 3, 'Electrical', 'odio consequat varius integer ac leo pellentesque ultrices mattis odio donec vitae nisi nam', 'In progress', '2025-01-06 05:48:23', NULL, 5, '2025-08-22 04:09:51', 'http://dummyimage.com/210x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (43, 31, 2, 5, 'Other', 'in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris', 'Completed', '2025-02-21 03:36:41', '2025-10-03 22:17:38', 4, '2024-12-14 18:21:30', 'http://dummyimage.com/210x100.png/ff4444/ffffff', 'risus semper porta volutpat quam pede lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus');
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (44, 30, 5, 5, 'Plumbing', 'aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis', 'Blocked', '2024-12-04 03:03:06', NULL, 3, '2025-03-30 09:27:23', 'http://dummyimage.com/113x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (45, 10, 7, 5, 'Other', 'erat nulla tempus vivamus in felis eu sapien cursus vestibulum proin eu mi nulla ac enim in', 'In progress', '2025-06-26 07:49:58', NULL, 4, '2025-06-16 04:40:49', 'http://dummyimage.com/192x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (46, 17, 5, 2, 'Plumbing', 'congue risus semper porta volutpat quam pede lobortis ligula sit amet eleifend pede libero quis orci', 'In progress', '2025-06-23 14:38:46', NULL, 1, '2024-12-19 18:26:54', 'http://dummyimage.com/170x100.png/5fa2dd/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (47, 14, 7, 3, 'Plumbing', 'quisque ut erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam augue quam', 'Blocked', '2024-12-07 02:54:21', NULL, 0, '2025-06-05 23:01:16', 'http://dummyimage.com/199x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (48, 31, 1, 1, 'Electrical', 'in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis', 'In progress', '2025-06-01 23:31:28', NULL, 3, '2025-11-12 19:50:10', 'http://dummyimage.com/215x100.png/cc0000/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (49, 20, 9, 4, 'Structural', 'luctus ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum', 'Blocked', '2025-04-28 09:06:34', NULL, 1, '2025-06-18 09:15:43', 'http://dummyimage.com/124x100.png/ff4444/ffffff', NULL);
insert into maintenanceRequest (requestID, studentRequestingID, buildingID, aptNumber, issueType, issueDescription, activeStatus, dateRequested, dateCompleted, priority, scheduledDate, issuePhotos, completionNotes) values (50, 6, 8, 4, 'Structural', 'in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at', 'Blocked', '2024-12-24 00:33:03', NULL, 1, '2025-04-19 06:34:39', 'http://dummyimage.com/161x100.png/5fa2dd/ffffff', NULL);

insert into part (partID, name, cost, quantity) values (1, 'Wall Art', 98, 5);
insert into part (partID, name, cost, quantity) values (2, 'Protein Bar Variety Pack', 92, 64);
insert into part (partID, name, cost, quantity) values (3, 'Salt and Pepper Grinder Set', 28, 75);
insert into part (partID, name, cost, quantity) values (4, 'Silicone Baking Mats', 86, 14);
insert into part (partID, name, cost, quantity) values (5, 'Mediterranean Olives', 68, 99);
insert into part (partID, name, cost, quantity) values (6, 'Savory Breakfast Sausage', 12, 84);
insert into part (partID, name, cost, quantity) values (7, 'Art Supplies Organizer', 90, 2);
insert into part (partID, name, cost, quantity) values (8, 'Honey Nut Cheerios', 50, 28);
insert into part (partID, name, cost, quantity) values (9, 'Energy Protein Bars', 73, 79);
insert into part (partID, name, cost, quantity) values (10, 'Sweet BBQ Dipping Sauce', 36, 72);
insert into part (partID, name, cost, quantity) values (11, 'Organic Black Rice', 9, 5);
insert into part (partID, name, cost, quantity) values (12, 'Travel Yoga Mat', 16, 31);
insert into part (partID, name, cost, quantity) values (13, 'Dish Rack', 71, 41);
insert into part (partID, name, cost, quantity) values (14, 'Pumpkin Ice Cream', 72, 65);
insert into part (partID, name, cost, quantity) values (15, 'Paprika', 42, 36);
insert into part (partID, name, cost, quantity) values (16, 'Vegan Cheese', 18, 11);
insert into part (partID, name, cost, quantity) values (17, 'Almond Milk', 44, 18);
insert into part (partID, name, cost, quantity) values (18, 'Pine Nuts', 33, 78);
insert into part (partID, name, cost, quantity) values (19, 'Eco-Friendly Yoga Mat', 64, 11);
insert into part (partID, name, cost, quantity) values (20, 'Pasta Portion Control Measure', 5, 99);
insert into part (partID, name, cost, quantity) values (21, 'Vegetable Chips', 27, 5);
insert into part (partID, name, cost, quantity) values (22, 'Bamboo Toothbrush Holder', 5, 70);
insert into part (partID, name, cost, quantity) values (23, 'Shoe Organizer', 16, 8);
insert into part (partID, name, cost, quantity) values (24, 'Coconut Bowls Set', 42, 30);
insert into part (partID, name, cost, quantity) values (25, 'Applewood Smoked Bacon', 79, 90);
insert into part (partID, name, cost, quantity) values (26, 'Travel Orthopedic Pillow', 41, 85);
insert into part (partID, name, cost, quantity) values (27, 'Pumpkin Spice Pancake Mix', 1, 19);
insert into part (partID, name, cost, quantity) values (28, 'Over-Ear Headphones', 100, 27);
insert into part (partID, name, cost, quantity) values (29, 'Almond Joy Protein Bars', 42, 1);
insert into part (partID, name, cost, quantity) values (30, 'Hydration Backpack', 99, 75);

insert into tool (toolID, name, quantity) values (1, 'Bulldozer', 29);
insert into tool (toolID, name, quantity) values (2, 'Scraper', 36);
insert into tool (toolID, name, quantity) values (3, 'Bulldozer', 46);
insert into tool (toolID, name, quantity) values (4, 'Grader', 36);
insert into tool (toolID, name, quantity) values (5, 'Scraper', 12);
insert into tool (toolID, name, quantity) values (6, 'Crawler', 25);
insert into tool (toolID, name, quantity) values (7, 'Backhoe', 25);
insert into tool (toolID, name, quantity) values (8, 'Backhoe', 30);
insert into tool (toolID, name, quantity) values (9, 'Skid-Steer', 48);
insert into tool (toolID, name, quantity) values (10, 'Excavator', 37);
insert into tool (toolID, name, quantity) values (11, 'Excavator', 25);
insert into tool (toolID, name, quantity) values (12, 'Skid-Steer', 28);
insert into tool (toolID, name, quantity) values (13, 'Crawler', 41);
insert into tool (toolID, name, quantity) values (14, 'Dragline', 32);
insert into tool (toolID, name, quantity) values (15, 'Skid-Steer', 13);
insert into tool (toolID, name, quantity) values (16, 'Excavator', 19);
insert into tool (toolID, name, quantity) values (17, 'Backhoe', 37);
insert into tool (toolID, name, quantity) values (18, 'Trencher', 8);
insert into tool (toolID, name, quantity) values (19, 'Dump Truck', 5);
insert into tool (toolID, name, quantity) values (20, 'Excavator', 46);
insert into tool (toolID, name, quantity) values (21, 'Compactor', 3);
insert into tool (toolID, name, quantity) values (22, 'Scraper', 30);
insert into tool (toolID, name, quantity) values (23, 'Trencher', 37);
insert into tool (toolID, name, quantity) values (24, 'Scraper', 34);
insert into tool (toolID, name, quantity) values (25, 'Dump Truck', 42);
insert into tool (toolID, name, quantity) values (26, 'Grader', 28);
insert into tool (toolID, name, quantity) values (27, 'Trencher', 44);
insert into tool (toolID, name, quantity) values (28, 'Scraper', 13);
insert into tool (toolID, name, quantity) values (29, 'Bulldozer', 50);
insert into tool (toolID, name, quantity) values (30, 'Dragline', 31);


insert into partUsed (partID, requestID) values (16, 40);
insert into partUsed (partID, requestID) values (15, 37);
insert into partUsed (partID, requestID) values (10, 22);
insert into partUsed (partID, requestID) values (5, 13);
insert into partUsed (partID, requestID) values (3, 24);
insert into partUsed (partID, requestID) values (11, 5);
insert into partUsed (partID, requestID) values (17, 32);
insert into partUsed (partID, requestID) values (19, 9);
insert into partUsed (partID, requestID) values (8, 30);
insert into partUsed (partID, requestID) values (15, 32);
insert into partUsed (partID, requestID) values (12, 31);
insert into partUsed (partID, requestID) values (13, 36);
insert into partUsed (partID, requestID) values (21, 32);
insert into partUsed (partID, requestID) values (7, 5);
insert into partUsed (partID, requestID) values (10, 32);
insert into partUsed (partID, requestID) values (19, 13);
insert into partUsed (partID, requestID) values (4, 13);
insert into partUsed (partID, requestID) values (14, 32);
insert into partUsed (partID, requestID) values (18, 8);
insert into partUsed (partID, requestID) values (26, 3);
insert into partUsed (partID, requestID) values (4, 5);
insert into partUsed (partID, requestID) values (19, 25);
insert into partUsed (partID, requestID) values (1, 9);
insert into partUsed (partID, requestID) values (13, 23);
insert into partUsed (partID, requestID) values (4, 40);
insert into partUsed (partID, requestID) values (18, 29);
insert into partUsed (partID, requestID) values (3, 39);
insert into partUsed (partID, requestID) values (10, 40);
insert into partUsed (partID, requestID) values (17, 40);
insert into partUsed (partID, requestID) values (8, 37);
insert into partUsed (partID, requestID) values (23, 19);
insert into partUsed (partID, requestID) values (21, 33);
insert into partUsed (partID, requestID) values (4, 18);
insert into partUsed (partID, requestID) values (15, 20);
insert into partUsed (partID, requestID) values (21, 7);
insert into partUsed (partID, requestID) values (20, 32);
insert into partUsed (partID, requestID) values (17, 21);
insert into partUsed (partID, requestID) values (13, 8);
insert into partUsed (partID, requestID) values (16, 21);
insert into partUsed (partID, requestID) values (22, 32);
insert into partUsed (partID, requestID) values (22, 8);
insert into partUsed (partID, requestID) values (17, 7);
insert into partUsed (partID, requestID) values (11, 23);
insert into partUsed (partID, requestID) values (26, 19);
insert into partUsed (partID, requestID) values (5, 30);
insert into partUsed (partID, requestID) values (20, 39);
insert into partUsed (partID, requestID) values (9, 17);
insert into partUsed (partID, requestID) values (1, 13);
insert into partUsed (partID, requestID) values (30, 12);
insert into partUsed (partID, requestID) values (16, 27);
insert into partUsed (partID, requestID) values (27, 30);
insert into partUsed (partID, requestID) values (25, 31);
insert into partUsed (partID, requestID) values (24, 28);
insert into partUsed (partID, requestID) values (15, 13);
insert into partUsed (partID, requestID) values (27, 6);
insert into partUsed (partID, requestID) values (23, 40);
insert into partUsed (partID, requestID) values (5, 3);
insert into partUsed (partID, requestID) values (16, 5);
insert into partUsed (partID, requestID) values (1, 12);
insert into partUsed (partID, requestID) values (9, 11);
insert into partUsed (partID, requestID) values (3, 14);
insert into partUsed (partID, requestID) values (19, 5);
insert into partUsed (partID, requestID) values (18, 37);
insert into partUsed (partID, requestID) values (19, 34);
insert into partUsed (partID, requestID) values (27, 21);
insert into partUsed (partID, requestID) values (10, 19);
insert into partUsed (partID, requestID) values (28, 7);
insert into partUsed (partID, requestID) values (27, 28);
insert into partUsed (partID, requestID) values (2, 15);
insert into partUsed (partID, requestID) values (24, 24);
insert into partUsed (partID, requestID) values (27, 23);
insert into partUsed (partID, requestID) values (3, 38);
insert into partUsed (partID, requestID) values (22, 26);
insert into partUsed (partID, requestID) values (23, 9);
insert into partUsed (partID, requestID) values (3, 6);
insert into partUsed (partID, requestID) values (30, 34);
insert into partUsed (partID, requestID) values (18, 39);
insert into partUsed (partID, requestID) values (23, 39);
insert into partUsed (partID, requestID) values (11, 15);
insert into partUsed (partID, requestID) values (2, 39);
insert into partUsed (partID, requestID) values (14, 1);
insert into partUsed (partID, requestID) values (25, 23);
insert into partUsed (partID, requestID) values (15, 36);
insert into partUsed (partID, requestID) values (9, 25);
insert into partUsed (partID, requestID) values (10, 7);
insert into partUsed (partID, requestID) values (17, 36);
insert into partUsed (partID, requestID) values (24, 15);
insert into partUsed (partID, requestID) values (26, 8);
insert into partUsed (partID, requestID) values (7, 6);
insert into partUsed (partID, requestID) values (18, 27);
insert into partUsed (partID, requestID) values (12, 7);
insert into partUsed (partID, requestID) values (7, 26);
insert into partUsed (partID, requestID) values (11, 26);
insert into partUsed (partID, requestID) values (20, 20);
insert into partUsed (partID, requestID) values (15, 15);
insert into partUsed (partID, requestID) values (7, 14);
insert into partUsed (partID, requestID) values (29, 40);
insert into partUsed (partID, requestID) values (2, 18);
insert into partUsed (partID, requestID) values (26, 17);
insert into partUsed (partID, requestID) values (10, 18);
insert into partUsed (partID, requestID) values (21, 8);
insert into partUsed (partID, requestID) values (20, 11);
insert into partUsed (partID, requestID) values (24, 6);
insert into partUsed (partID, requestID) values (9, 26);
insert into partUsed (partID, requestID) values (27, 20);
insert into partUsed (partID, requestID) values (19, 27);
insert into partUsed (partID, requestID) values (23, 3);
insert into partUsed (partID, requestID) values (1, 4);
insert into partUsed (partID, requestID) values (12, 29);
insert into partUsed (partID, requestID) values (4, 11);
insert into partUsed (partID, requestID) values (29, 10);
insert into partUsed (partID, requestID) values (12, 24);
insert into partUsed (partID, requestID) values (26, 23);
insert into partUsed (partID, requestID) values (24, 16);
insert into partUsed (partID, requestID) values (3, 40);
insert into partUsed (partID, requestID) values (25, 29);
insert into partUsed (partID, requestID) values (1, 14);
insert into partUsed (partID, requestID) values (28, 15);
insert into partUsed (partID, requestID) values (5, 22);
insert into partUsed (partID, requestID) values (22, 38);
insert into partUsed (partID, requestID) values (18, 25);
insert into partUsed (partID, requestID) values (16, 31);
insert into partUsed (partID, requestID) values (11, 20);
insert into partUsed (partID, requestID) values (30, 33);
insert into partUsed (partID, requestID) values (17, 1);


insert into toolUsed (toolID, requestID) values (20, 13);
insert into toolUsed (toolID, requestID) values (18, 31);
insert into toolUsed (toolID, requestID) values (17, 17);
insert into toolUsed (toolID, requestID) values (29, 27);
insert into toolUsed (toolID, requestID) values (7, 20);
insert into toolUsed (toolID, requestID) values (12, 33);
insert into toolUsed (toolID, requestID) values (16, 27);
insert into toolUsed (toolID, requestID) values (27, 14);
insert into toolUsed (toolID, requestID) values (18, 5);
insert into toolUsed (toolID, requestID) values (18, 26);
insert into toolUsed (toolID, requestID) values (9, 21);
insert into toolUsed (toolID, requestID) values (20, 27);
insert into toolUsed (toolID, requestID) values (11, 4);
insert into toolUsed (toolID, requestID) values (11, 32);
insert into toolUsed (toolID, requestID) values (23, 29);
insert into toolUsed (toolID, requestID) values (27, 36);
insert into toolUsed (toolID, requestID) values (21, 6);
insert into toolUsed (toolID, requestID) values (21, 40);
insert into toolUsed (toolID, requestID) values (29, 3);
insert into toolUsed (toolID, requestID) values (9, 25);
insert into toolUsed (toolID, requestID) values (18, 33);
insert into toolUsed (toolID, requestID) values (30, 27);
insert into toolUsed (toolID, requestID) values (2, 22);
insert into toolUsed (toolID, requestID) values (16, 37);
insert into toolUsed (toolID, requestID) values (27, 15);
insert into toolUsed (toolID, requestID) values (27, 31);
insert into toolUsed (toolID, requestID) values (3, 18);
insert into toolUsed (toolID, requestID) values (5, 39);
insert into toolUsed (toolID, requestID) values (18, 11);
insert into toolUsed (toolID, requestID) values (16, 32);
insert into toolUsed (toolID, requestID) values (2, 8);
insert into toolUsed (toolID, requestID) values (30, 1);
insert into toolUsed (toolID, requestID) values (2, 19);
insert into toolUsed (toolID, requestID) values (3, 19);
insert into toolUsed (toolID, requestID) values (10, 15);
insert into toolUsed (toolID, requestID) values (25, 3);
insert into toolUsed (toolID, requestID) values (6, 21);
insert into toolUsed (toolID, requestID) values (27, 4);
insert into toolUsed (toolID, requestID) values (19, 13);
insert into toolUsed (toolID, requestID) values (21, 25);
insert into toolUsed (toolID, requestID) values (9, 26);
insert into toolUsed (toolID, requestID) values (13, 11);
insert into toolUsed (toolID, requestID) values (2, 37);
insert into toolUsed (toolID, requestID) values (25, 35);
insert into toolUsed (toolID, requestID) values (17, 16);
insert into toolUsed (toolID, requestID) values (22, 10);
insert into toolUsed (toolID, requestID) values (28, 20);
insert into toolUsed (toolID, requestID) values (15, 11);
insert into toolUsed (toolID, requestID) values (25, 21);
insert into toolUsed (toolID, requestID) values (12, 39);
insert into toolUsed (toolID, requestID) values (9, 13);
insert into toolUsed (toolID, requestID) values (12, 28);
insert into toolUsed (toolID, requestID) values (13, 24);
insert into toolUsed (toolID, requestID) values (23, 4);
insert into toolUsed (toolID, requestID) values (15, 23);
insert into toolUsed (toolID, requestID) values (5, 11);
insert into toolUsed (toolID, requestID) values (18, 6);
insert into toolUsed (toolID, requestID) values (2, 3);
insert into toolUsed (toolID, requestID) values (16, 35);
insert into toolUsed (toolID, requestID) values (27, 38);
insert into toolUsed (toolID, requestID) values (12, 38);
insert into toolUsed (toolID, requestID) values (25, 7);
insert into toolUsed (toolID, requestID) values (24, 33);
insert into toolUsed (toolID, requestID) values (12, 27);
insert into toolUsed (toolID, requestID) values (27, 16);
insert into toolUsed (toolID, requestID) values (16, 13);
insert into toolUsed (toolID, requestID) values (5, 3);
insert into toolUsed (toolID, requestID) values (27, 12);
insert into toolUsed (toolID, requestID) values (1, 10);
insert into toolUsed (toolID, requestID) values (2, 38);
insert into toolUsed (toolID, requestID) values (19, 9);
insert into toolUsed (toolID, requestID) values (4, 6);
insert into toolUsed (toolID, requestID) values (26, 17);
insert into toolUsed (toolID, requestID) values (11, 7);
insert into toolUsed (toolID, requestID) values (8, 11);
insert into toolUsed (toolID, requestID) values (17, 11);
insert into toolUsed (toolID, requestID) values (3, 24);
insert into toolUsed (toolID, requestID) values (26, 40);
insert into toolUsed (toolID, requestID) values (25, 29);
insert into toolUsed (toolID, requestID) values (13, 19);
insert into toolUsed (toolID, requestID) values (24, 11);
insert into toolUsed (toolID, requestID) values (17, 32);
insert into toolUsed (toolID, requestID) values (4, 13);
insert into toolUsed (toolID, requestID) values (28, 6);
insert into toolUsed (toolID, requestID) values (6, 37);
insert into toolUsed (toolID, requestID) values (28, 17);
insert into toolUsed (toolID, requestID) values (4, 9);
insert into toolUsed (toolID, requestID) values (9, 12);
insert into toolUsed (toolID, requestID) values (3, 10);
insert into toolUsed (toolID, requestID) values (30, 15);
insert into toolUsed (toolID, requestID) values (29, 1);
insert into toolUsed (toolID, requestID) values (3, 22);
insert into toolUsed (toolID, requestID) values (9, 28);
insert into toolUsed (toolID, requestID) values (24, 9);
insert into toolUsed (toolID, requestID) values (5, 31);
insert into toolUsed (toolID, requestID) values (3, 13);
insert into toolUsed (toolID, requestID) values (13, 10);
insert into toolUsed (toolID, requestID) values (26, 32);
insert into toolUsed (toolID, requestID) values (22, 33);
insert into toolUsed (toolID, requestID) values (12, 36);
insert into toolUsed (toolID, requestID) values (27, 29);
insert into toolUsed (toolID, requestID) values (12, 3);
insert into toolUsed (toolID, requestID) values (29, 28);
insert into toolUsed (toolID, requestID) values (23, 40);
insert into toolUsed (toolID, requestID) values (1, 39);
insert into toolUsed (toolID, requestID) values (25, 31);
insert into toolUsed (toolID, requestID) values (22, 20);
insert into toolUsed (toolID, requestID) values (11, 36);
insert into toolUsed (toolID, requestID) values (22, 19);
insert into toolUsed (toolID, requestID) values (14, 37);
insert into toolUsed (toolID, requestID) values (26, 36);
insert into toolUsed (toolID, requestID) values (10, 14);
insert into toolUsed (toolID, requestID) values (23, 32);
insert into toolUsed (toolID, requestID) values (26, 35);
insert into toolUsed (toolID, requestID) values (17, 23);
insert into toolUsed (toolID, requestID) values (9, 24);
insert into toolUsed (toolID, requestID) values (25, 37);
insert into toolUsed (toolID, requestID) values (15, 6);
insert into toolUsed (toolID, requestID) values (13, 17);
insert into toolUsed (toolID, requestID) values (14, 38);
insert into toolUsed (toolID, requestID) values (27, 35);
insert into toolUsed (toolID, requestID) values (7, 24);
insert into toolUsed (toolID, requestID) values (27, 39);
insert into toolUsed (toolID, requestID) values (3, 39);
insert into toolUsed (toolID, requestID) values (30, 32);


insert into employeeAssigned (employeeID, requestID) values (6, 15);
insert into employeeAssigned (employeeID, requestID) values (8, 7);
insert into employeeAssigned (employeeID, requestID) values (6, 26);
insert into employeeAssigned (employeeID, requestID) values (30, 28);
insert into employeeAssigned (employeeID, requestID) values (4, 29);
insert into employeeAssigned (employeeID, requestID) values (11, 11);
insert into employeeAssigned (employeeID, requestID) values (14, 10);
insert into employeeAssigned (employeeID, requestID) values (14, 11);
insert into employeeAssigned (employeeID, requestID) values (10, 8);
insert into employeeAssigned (employeeID, requestID) values (10, 15);
insert into employeeAssigned (employeeID, requestID) values (4, 35);
insert into employeeAssigned (employeeID, requestID) values (16, 7);
insert into employeeAssigned (employeeID, requestID) values (23, 35);
insert into employeeAssigned (employeeID, requestID) values (25, 19);
insert into employeeAssigned (employeeID, requestID) values (13, 26);
insert into employeeAssigned (employeeID, requestID) values (21, 10);
insert into employeeAssigned (employeeID, requestID) values (11, 12);
insert into employeeAssigned (employeeID, requestID) values (26, 34);
insert into employeeAssigned (employeeID, requestID) values (27, 28);
insert into employeeAssigned (employeeID, requestID) values (22, 5);
insert into employeeAssigned (employeeID, requestID) values (10, 23);
insert into employeeAssigned (employeeID, requestID) values (27, 13);
insert into employeeAssigned (employeeID, requestID) values (21, 3);
insert into employeeAssigned (employeeID, requestID) values (2, 20);
insert into employeeAssigned (employeeID, requestID) values (1, 27);
insert into employeeAssigned (employeeID, requestID) values (22, 10);
insert into employeeAssigned (employeeID, requestID) values (5, 35);
insert into employeeAssigned (employeeID, requestID) values (21, 31);
insert into employeeAssigned (employeeID, requestID) values (27, 2);
insert into employeeAssigned (employeeID, requestID) values (23, 20);
insert into employeeAssigned (employeeID, requestID) values (4, 23);
insert into employeeAssigned (employeeID, requestID) values (3, 27);
insert into employeeAssigned (employeeID, requestID) values (14, 19);
insert into employeeAssigned (employeeID, requestID) values (20, 3);
insert into employeeAssigned (employeeID, requestID) values (8, 28);
insert into employeeAssigned (employeeID, requestID) values (1, 5);
insert into employeeAssigned (employeeID, requestID) values (21, 28);
insert into employeeAssigned (employeeID, requestID) values (7, 6);
insert into employeeAssigned (employeeID, requestID) values (7, 37);
insert into employeeAssigned (employeeID, requestID) values (7, 20);
insert into employeeAssigned (employeeID, requestID) values (4, 39);
insert into employeeAssigned (employeeID, requestID) values (28, 25);
insert into employeeAssigned (employeeID, requestID) values (11, 29);
insert into employeeAssigned (employeeID, requestID) values (12, 12);
insert into employeeAssigned (employeeID, requestID) values (23, 25);
insert into employeeAssigned (employeeID, requestID) values (25, 39);
insert into employeeAssigned (employeeID, requestID) values (8, 9);
insert into employeeAssigned (employeeID, requestID) values (22, 14);
insert into employeeAssigned (employeeID, requestID) values (28, 4);
insert into employeeAssigned (employeeID, requestID) values (20, 17);
insert into employeeAssigned (employeeID, requestID) values (8, 19);
insert into employeeAssigned (employeeID, requestID) values (15, 29);
insert into employeeAssigned (employeeID, requestID) values (20, 13);
insert into employeeAssigned (employeeID, requestID) values (23, 26);
insert into employeeAssigned (employeeID, requestID) values (30, 24);
insert into employeeAssigned (employeeID, requestID) values (25, 7);
insert into employeeAssigned (employeeID, requestID) values (11, 28);
insert into employeeAssigned (employeeID, requestID) values (14, 2);
insert into employeeAssigned (employeeID, requestID) values (24, 14);
insert into employeeAssigned (employeeID, requestID) values (20, 1);
insert into employeeAssigned (employeeID, requestID) values (10, 36);
insert into employeeAssigned (employeeID, requestID) values (30, 8);
insert into employeeAssigned (employeeID, requestID) values (7, 31);
insert into employeeAssigned (employeeID, requestID) values (5, 8);
insert into employeeAssigned (employeeID, requestID) values (11, 23);
insert into employeeAssigned (employeeID, requestID) values (18, 17);
insert into employeeAssigned (employeeID, requestID) values (28, 29);
insert into employeeAssigned (employeeID, requestID) values (26, 12);
insert into employeeAssigned (employeeID, requestID) values (21, 11);
insert into employeeAssigned (employeeID, requestID) values (2, 35);
insert into employeeAssigned (employeeID, requestID) values (6, 6);
insert into employeeAssigned (employeeID, requestID) values (23, 27);
insert into employeeAssigned (employeeID, requestID) values (14, 18);
insert into employeeAssigned (employeeID, requestID) values (28, 11);
insert into employeeAssigned (employeeID, requestID) values (1, 36);
insert into employeeAssigned (employeeID, requestID) values (9, 14);
insert into employeeAssigned (employeeID, requestID) values (22, 34);
insert into employeeAssigned (employeeID, requestID) values (4, 16);
insert into employeeAssigned (employeeID, requestID) values (23, 33);
insert into employeeAssigned (employeeID, requestID) values (13, 3);
insert into employeeAssigned (employeeID, requestID) values (11, 17);
insert into employeeAssigned (employeeID, requestID) values (5, 19);
insert into employeeAssigned (employeeID, requestID) values (3, 38);
insert into employeeAssigned (employeeID, requestID) values (28, 38);
insert into employeeAssigned (employeeID, requestID) values (10, 39);
insert into employeeAssigned (employeeID, requestID) values (20, 19);
insert into employeeAssigned (employeeID, requestID) values (28, 12);
insert into employeeAssigned (employeeID, requestID) values (4, 36);
insert into employeeAssigned (employeeID, requestID) values (20, 10);
insert into employeeAssigned (employeeID, requestID) values (15, 39);
insert into employeeAssigned (employeeID, requestID) values (18, 20);
insert into employeeAssigned (employeeID, requestID) values (5, 22);
insert into employeeAssigned (employeeID, requestID) values (24, 6);
insert into employeeAssigned (employeeID, requestID) values (15, 1);
insert into employeeAssigned (employeeID, requestID) values (30, 38);
insert into employeeAssigned (employeeID, requestID) values (28, 30);
insert into employeeAssigned (employeeID, requestID) values (4, 30);
insert into employeeAssigned (employeeID, requestID) values (23, 16);
insert into employeeAssigned (employeeID, requestID) values (19, 20);
insert into employeeAssigned (employeeID, requestID) values (22, 37);
insert into employeeAssigned (employeeID, requestID) values (11, 19);
insert into employeeAssigned (employeeID, requestID) values (24, 20);
insert into employeeAssigned (employeeID, requestID) values (4, 3);
insert into employeeAssigned (employeeID, requestID) values (30, 27);
insert into employeeAssigned (employeeID, requestID) values (5, 11);
insert into employeeAssigned (employeeID, requestID) values (17, 33);
insert into employeeAssigned (employeeID, requestID) values (14, 31);
insert into employeeAssigned (employeeID, requestID) values (16, 24);
insert into employeeAssigned (employeeID, requestID) values (18, 3);
insert into employeeAssigned (employeeID, requestID) values (25, 6);
insert into employeeAssigned (employeeID, requestID) values (18, 8);
insert into employeeAssigned (employeeID, requestID) values (22, 29);
insert into employeeAssigned (employeeID, requestID) values (8, 11);
insert into employeeAssigned (employeeID, requestID) values (12, 6);
insert into employeeAssigned (employeeID, requestID) values (10, 12);
insert into employeeAssigned (employeeID, requestID) values (23, 14);
insert into employeeAssigned (employeeID, requestID) values (11, 38);
insert into employeeAssigned (employeeID, requestID) values (8, 13);
insert into employeeAssigned (employeeID, requestID) values (5, 23);
insert into employeeAssigned (employeeID, requestID) values (24, 4);
insert into employeeAssigned (employeeID, requestID) values (30, 23);
insert into employeeAssigned (employeeID, requestID) values (25, 30);
insert into employeeAssigned (employeeID, requestID) values (5, 16);
insert into employeeAssigned (employeeID, requestID) values (7, 22);
insert into employeeAssigned (employeeID, requestID) values (18, 38);

