create database Library;
use Library;

-- Creating the Genres table
CREATE TABLE Genres (
    GenreID INT PRIMARY KEY,
    GenreName VARCHAR(50) NOT NULL
);

-- Creating the Authors table
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY,
    AuthorName VARCHAR(100) NOT NULL
);

-- Creating the Books table with foreign keys
CREATE TABLE Books (
    BookID INT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    AuthorID INT,
    Copies INT NOT NULL CHECK (Copies >= 0),
    GenreID INT,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
);

-- Inserting Genres
INSERT INTO Genres (GenreID, GenreName) VALUES
(1, 'Fiction'),
(2, 'Non-Fiction'),
(3, 'Science Fiction'),
(4, 'Fantasy'),
(5, 'Mystery'),
(6, 'Biography'),
(7, 'History'),
(8, 'Romance'),
(9, 'Thriller'),
(10, 'Self-Help');

-- Inserting Authors
INSERT INTO Authors (AuthorID, AuthorName) VALUES
(1, 'Jane Austen'),
(2, 'George Orwell'),
(3, 'J.K. Rowling'),
(4, 'Stephen King'),
(5, 'Agatha Christie'),
(6, 'Yuval Noah Harari'),
(7, 'Tolkien'),
(8, 'Dan Brown'),
(9, 'Michelle Obama'),
(10, 'James Clear'),
(11, 'Ernest Hemingway'),
(12, 'F. Scott Fitzgerald'),
(13, 'Virginia Woolf'),
(14, 'Gabriel Garcia Marquez'),
(15, 'Toni Morrison'),
(16, 'Isaac Asimov'),
(17, 'Philip K. Dick'),
(18, 'Ray Bradbury'),
(19, 'Arthur C. Clarke'),
(20, 'Ursula K. Le Guin');

-- Inserting Books (100 records)
INSERT INTO Books (BookID, Title, AuthorID, Copies, GenreID) VALUES
(1, 'Pride and Prejudice', 1, 5, 8),
(2, '1984', 2, 8, 3),
(3, 'Harry Potter and the Philosopher''s Stone', 3, 10, 4),
(4, 'The Shining', 4, 6, 9),
(5, 'Murder on the Orient Express', 5, 7, 5),
(6, 'Sapiens: A Brief History of Humankind', 6, 4, 7),
(7, 'The Hobbit', 7, 9, 4),
(8, 'The Da Vinci Code', 8, 6, 9),
(9, 'Becoming', 9, 5, 6),
(10, 'Atomic Habits', 10, 8, 10),
(11, 'The Old Man and the Sea', 11, 4, 1),
(12, 'The Great Gatsby', 12, 7, 1),
(13, 'Mrs. Dalloway', 13, 3, 1),
(14, 'One Hundred Years of Solitude', 14, 5, 1),
(15, 'Beloved', 15, 4, 1),
(16, 'Foundation', 16, 6, 3),
(17, 'Do Androids Dream of Electric Sheep?', 17, 5, 3),
(18, 'Fahrenheit 451', 18, 7, 3),
(19, '2001: A Space Odyssey', 19, 4, 3),
(20, 'The Left Hand of Darkness', 20, 5, 3),
(21, 'Sense and Sensibility', 1, 4, 8),
(22, 'Animal Farm', 2, 6, 1),
(23, 'Harry Potter and the Chamber of Secrets', 3, 9, 4),
(24, 'It', 4, 5, 9),
(25, 'And Then There Were None', 5, 6, 5),
(26, 'Homo Deus', 6, 3, 7),
(27, 'The Lord of the Rings', 7, 8, 4),
(28, 'Angels and Demons', 8, 5, 9),
(29, 'A Brief History of Time', 4, 4, 2),
(30, 'The Power of Habit', 10, 6, 10),
(31, 'A Farewell to Arms', 11, 5, 1),
(32, 'Tender is the Night', 12, 4, 1),
(33, 'To the Lighthouse', 13, 3, 1),
(34, 'Love in the Time of Cholera', 14, 5, 8),
(35, 'Song of Solomon', 15, 4, 1),
(36, 'I, Robot', 16, 6, 3),
(37, 'The Man in the High Castle', 17, 5, 3),
(38, 'The Martian Chronicles', 18, 4, 3),
(39, 'Childhood''s End', 19, 5, 3),
(40, 'A Wizard of Earthsea', 20, 6, 4),
(41, 'Emma', 1, 4, 8),
(42, 'Keep the Aspidistra Flying', 2, 3, 1),
(43, 'Harry Potter and the Prisoner of Azkaban', 3, 8, 4),
(44, 'Carrie', 4, 5, 9),
(45, 'The ABC Murders', 5, 6, 5),
(46, '21 Lessons for the 21st Century', 6, 4, 7),
(47, 'The Silmarillion', 7, 5, 4),
(48, 'Inferno', 8, 6, 9),
(49, 'The Audacity of Hope', 9, 4, 6),
(50, 'Thinking, Fast and Slow', 10, 5, 10),
(51, 'For Whom the Bell Tolls', 11, 4, 1),
(52, 'This Side of Paradise', 12, 3, 1),
(53, 'Orlando', 13, 4, 1),
(54, 'Chronicle of a Death Foretold', 14, 5, 5),
(55, 'Jazz', 15, 4, 1),
(56, 'The Caves of Steel', 16, 5, 3),
(57, 'Ubik', 17, 4, 3),
(58, 'Something Wicked This Way Comes', 18, 5, 4),
(59, 'Rendezvous with Rama', 19, 4, 3),
(60, 'The Dispossessed', 20, 5, 3),
(61, 'Persuasion', 1, 4, 8),
(62, 'Down and Out in Paris and London', 2, 3, 6),
(63, 'Harry Potter and the Goblet of Fire', 3, 7, 4),
(64, 'Salem''s Lot', 4, 5, 9),
(65, 'Death on the Nile', 5, 6, 5),
(66, 'The Lessons of History', 6, 4, 7),
(67, 'The Children of Hurin', 7, 5, 4),
(68, 'The Lost Symbol', 8, 6, 9),
(69, 'Dreams from My Father', 9, 4, 6),
(70, 'The 7 Habits of Highly Effective People', 10, 5, 10),
(71, 'The Sun Also Rises', 11, 4, 1),
(72, 'The Beautiful and Damned', 12, 3, 1),
(73, 'The Waves', 13, 4, 1),
(74, 'The Autumn of the Patriarch', 14, 5, 1),
(75, 'Paradise', 15, 4, 1),
(76, 'The End of Eternity', 16, 5, 3),
(77, 'A Scanner Darkly', 17, 4, 3),
(78, 'The Illustrated Man', 18, 5, 3),
(79, 'The Fountains of Paradise', 19, 4, 3),
(80, 'Tehanu', 20, 5, 4),
(81, 'Northanger Abbey', 1, 4, 8),
(82, 'Homage to Catalonia', 2, 3, 6),
(83, 'Harry Potter and the Order of the Phoenix', 3, 7, 4),
(84, 'Misery', 4, 5, 9),
(85, 'The Mysterious Affair at Styles', 5, 6, 5),
(86, 'Man''s Search for Meaning', 6, 4, 10),
(87, 'Unfinished Tales', 7, 5, 4),
(88, 'Origin', 8, 6, 9),
(89, 'The Light We Carry', 9, 4, 6),
(90, 'Influence: The Psychology of Persuasion', 10, 5, 10),
(91, 'Across the River and Into the Trees', 11, 4, 1),
(92, 'Flappers and Philosophers', 12, 3, 1),
(93, 'A Room of One''s Own', 13, 4, 2),
(94, 'The General in His Labyrinth', 14, 5, 1),
(95, 'Tar Baby', 15, 4, 1),
(96, 'Pebble in the Sky', 16, 5, 3),
(97, 'Flow My Tears, the Policeman Said', 17, 4, 3),
(98, 'Dandelion Wine', 18, 5, 1),
(99, 'The Songs of Distant Earth', 19, 4, 3),
(100, 'The Tombs of Atuan', 20, 5, 4);

CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    profile TEXT
);

INSERT INTO users (email, password, profile) VALUES ('admin@gmail.com', '12345', '{}');

-- Create borrowings table if not exists
CREATE TABLE IF NOT EXISTS borrowings (
    borrowing_id INT PRIMARY KEY AUTO_INCREMENT,
    user_email VARCHAR(255) NOT NULL,
    BookID INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (user_email) REFERENCES users(email),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);




USE Library;

-- Drop existing tables to ensure clean schema (comment out if data needs to be preserved)
DROP TABLE IF EXISTS borrowings;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS users;

-- Create Genres table
CREATE TABLE Genres (
    GenreID INT PRIMARY KEY AUTO_INCREMENT,
    GenreName VARCHAR(255) NOT NULL
);

-- Create Authors table
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    AuthorName VARCHAR(255) NOT NULL
);

-- Create Books table
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    AuthorID INT NOT NULL,
    Copies INT NOT NULL CHECK (Copies >= 0),
    GenreID INT NOT NULL,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
);

-- Create users table
CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

-- Create borrowings table
CREATE TABLE borrowings (
    borrowing_id INT PRIMARY KEY AUTO_INCREMENT,
    user_email VARCHAR(255) NOT NULL,
    BookID INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (user_email) REFERENCES users(email),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);


INSERT INTO Genres (GenreName) VALUES ('Romance'), ('Science Fiction'), ('Mystery'), ('Fantasy');
INSERT INTO Authors (AuthorName) VALUES ('Jane Austen'), ('George Orwell'), ('Agatha Christie'), ('J.K. Rowling');
INSERT INTO Books (Title, AuthorID, Copies, GenreID) VALUES
    ('Pride and Prejudice', 1, 5, 1),
    ('1984', 2, 8, 2),
    ('Murder on the Orient Express', 3, 3, 3),
    ('Harry Potter and the Philosopher''s Stone', 4, 10, 4);
INSERT INTO users (email, password) VALUES ('admin@gmail.com', '12345');

Select * from Books;

INSERT INTO Genres (GenreName) VALUES
('Fiction'),
('Non-Fiction'),
('Biography'),
('History'),
('Thriller'),
('Self-Help');

SELECT * FROM genres;

insert INTO Authors (AuthorName) VALUES
('Emily Harper'),
('Rajesh Patel'),
('Sofia Alvarez'),
('Liam O’Connor'),
('Aisha Khan'),
('Hiroshi Tanaka'),
('Clara Dubois'),
('Omar Farooq'),
('Isabella Rossi'),
('Kwame Nkrumah'),
('Mei Ling Chen'),
('Declan Murphy'),
('Fatima Zahra'),
('Viktor Ivanov'),
('Amara Nwosu'),
('Lucas Ferreira'),
('Ananya Sharma'),
('Elias Johansson'),
('Nadia Bouzid'),
('Javier Morales'),
('Priya Deshmukh'),
('Mikhail Volkov'),
('Zoe Campbell'),
('Arjun Reddy'),
('Leila Hassan'),
('Mateo Garcia'),
('Chloe Martin'),
('Sanjay Gupta'),
('Elena Petrova'),
('Noah Kim'),
('Amina Yusuf'),
('Gabriel Silva'),
('Riya Malhotra'),
('Lars Eriksson'),
('Samira Ali'),
('Diego Lopez'),
('Hannah Weber'),
('Vikram Singh'),
('Yara Mahmoud'),
('Finn O’Sullivan'),
('Lila Nguyen'),
('Rahul Joshi'),
('Camila Torres'),
('Theo Dubois'),
('Zainab Iqbal'),
('Sebastian Muller'),
('Anika Patel'),
('Oleg Romanov'),
('Maya Gonzalez'),
('Kiran Rao');

Select * from authors;

INSERT INTO Books (Title, AuthorID, Copies, GenreID) VALUES
    ('Whispers of Time', 1, 4, 1),
    ('Echoes of the Desert', 2, 7, 7),
    ('Starlit Dreams', 3, 3, 3),
    ('Quantum Shadows', 4, 6, 4),
    ('The Silent Clue', 5, 5, 5),
    ('Hearts in Bloom', 6, 8, 6),
    ('Empires of Dust', 7, 2, 7),
    ('Life in Letters', 8, 9, 8),
    ('Midnight Terrors', 9, 1, 9),
    ('Journey Beyond', 10, 4, 10),
    ('Tides of Fate', 11, 6, 1),
    ('Sands of Eternity', 12, 3, 7),
    ('Moonlit Quest', 13, 5, 3),
    ('Galactic Horizons', 14, 7, 4),
    ('Hidden Truths', 15, 2, 5),
    ('Love’s Last Dance', 16, 8, 6),
    ('Kings and Rebels', 17, 4, 7),
    ('Voice of Valor', 18, 6, 8),
    ('Grave Whispers', 19, 3, 9),
    ('Trails of Triumph', 20, 5, 10),
    ('River of Souls', 21, 7, 1),
    ('Chronicles of War', 22, 2, 7),
    ('Dragon’s Dawn', 23, 9, 3),
    ('Cosmic Drift', 24, 4, 4),
    ('The Locked Room', 25, 6, 5),
    ('Eternal Vows', 26, 3, 6),
    ('Fallen Thrones', 27, 8, 7),
    ('My Truth', 28, 5, 8),
    ('Shadows of Fear', 29, 2, 9),
    ('Horizon’s Edge', 30, 7, 10),
    ('Silent Waters', 31, 4, 1),
    ('Age of Valor', 32, 6, 7),
    ('Starborn Legacy', 33, 3, 3),
    ('Time’s Abyss', 34, 8, 4),
    ('Mystery of the Manor', 35, 5, 5),
    ('Forever Yours', 36, 2, 6),
    ('Rebels of Rome', 37, 7, 7),
    ('Path to Glory', 38, 4, 8),
    ('Nightmare’s Grip', 39, 6, 9),
    ('Quest for Freedom', 40, 3, 10),
    ('Waves of Destiny', 41, 8, 1),
    ('Echoes of Empire', 42, 5, 7),
    ('Fire and Sky', 43, 2, 3),
    ('Nebula’s Heart', 44, 7, 4),
    ('The Vanishing Key', 45, 4, 5),
    ('Love in Shadows', 46, 6, 6),
    ('Crown of Ages', 47, 3, 7),
    ('Soul’s Journey', 48, 8, 8),
    ('Dark Descent', 49, 5, 9),
    ('Beyond the Stars', 50, 2, 10);
    
select * from books;
ALTER TABLE users
ADD COLUMN profile TEXT ;

select * from users;