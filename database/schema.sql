-- schema.sql
CREATE TABLE USERS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'USER', -- USER, SHELTER_ADMIN, SUPER_ADMIN
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SHELTERS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES USERS(id),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    description TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    funds_allocated DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PETS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shelter_id UUID REFERENCES SHELTERS(id),
    name VARCHAR(255) NOT NULL,
    breed VARCHAR(255),
    age INT,
    gender VARCHAR(50),
    vaccination_status Boolean DEFAULT FALSE,
    personality TEXT,
    health_notes TEXT,
    is_adopted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PET_IMAGES (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES PETS(id),
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ADOPTION_REQUESTS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pet_id UUID REFERENCES PETS(id),
    user_id UUID REFERENCES USERS(id),
    shelter_id UUID REFERENCES SHELTERS(id),
    experience TEXT,
    house_type VARCHAR(255),
    reason TEXT,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE MESSAGES (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID REFERENCES USERS(id),
    receiver_id UUID REFERENCES USERS(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE DONATIONS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    donor_name VARCHAR(255),
    donor_email VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    stripe_payment_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'PENDING',
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE VOLUNTEERS (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES USERS(id),
    shelter_id UUID REFERENCES SHELTERS(id),
    age INT,
    city VARCHAR(255),
    skills TEXT,
    available_days TEXT,
    animal_experience TEXT,
    motivation_message TEXT,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
