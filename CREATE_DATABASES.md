# 🗄️ Creating Your Own MongoDB Databases

## 📊 **Required Databases: 2**

### **Database 1: Movies Database**
```
Database Name: YOUR_MOVIES_DB
Collection: Telegram_files
Purpose: Movie files and metadata
```

### **Database 2: Users Database**
```
Database Name: YOUR_USERS_DB  
Collections: users, chats, settings
Purpose: User management and bot settings
```

## 🔧 **Step 1: Create MongoDB Databases**

### **Option A: MongoDB Atlas (Free)**
1. Go to https://www.mongodb.com/atlas
2. Create free account
3. Create cluster
4. Create 2 databases:
   - `your_movies_db`
   - `your_users_db`

### **Option B: Local MongoDB**
```bash
# Install MongoDB locally
# Create databases
use your_movies_db
use your_users_db
```

## 📁 **Step 2: Database Schemas**

### **Movies Database Structure:**
```json
// Collection: Telegram_files
{
  "_id": "TELEGRAM_FILE_ID",           // Your bot's file ID
  "file_name": "Movie Name 2023.mkv", // Movie filename
  "file_size": 1234567890,            // File size in bytes
  "file_type": "video",               // File type
  "mime_type": "video/x-matroska",    // MIME type
  "caption": "Movie description",     // Optional caption
  "date": "2023-12-01",              // Upload date
  "channel_id": -1001234567890       // Channel where file is stored
}
```

### **Users Database Structure:**
```json
// Collection: users
{
  "_id": 123456789,                  // User's Telegram ID
  "first_name": "John",             // User's first name
  "username": "john_doe",           // Username (optional)
  "date": "2023-12-01",            // Join date
  "is_banned": false               // Ban status
}

// Collection: chats
{
  "_id": -1001234567890,           // Chat ID
  "title": "Movie Group",         // Chat title
  "type": "supergroup",           // Chat type
  "date": "2023-12-01"           // Added date
}

// Collection: settings
{
  "_id": "AUTH_CHANNEL",
  "value": "-1002614174192 -1001641168678"
}
```

## 🔧 **Step 3: Update Bot Configuration**

### **Update info.py:**
```python
# Your new database connections
DATABASE_URI = "mongodb+srv://username:password@cluster.mongodb.net/your_movies_db"
FILES_DB_URL = "mongodb+srv://username:password@cluster.mongodb.net/your_users_db"

# Database names
DATABASE_NAME = "your_movies_db"
COLLECTION_NAME = "Telegram_files"
```

## 📤 **Step 4: Upload Movies to Your Database**

### **Method 1: Manual Upload**
1. Upload movies to your channels
2. Get file IDs
3. Add to MongoDB manually

### **Method 2: Bot Upload Script**
```python
# Upload and auto-add to database
await upload_movie_to_channel_and_db(movie_file)
```

### **Method 3: Import Script**
```python
# Bulk import from files
await import_movies_from_folder(folder_path)
```

## 🚀 **Step 5: Populate Database**

### **Essential Collections:**

1. **Start with empty databases**
2. **Upload 5-10 test movies**
3. **Verify bot can send them**
4. **Gradually add more movies**

### **Minimum Movies for Testing:**
- 1 English movie
- 1 Korean movie  
- 1 Spanish movie
- 1 Hindi movie
- 1 Action movie

## 📋 **Complete Setup Checklist:**

### **Database Setup:**
- [ ] Create MongoDB Atlas account
- [ ] Create cluster
- [ ] Create `your_movies_db` database
- [ ] Create `your_users_db` database
- [ ] Get connection strings

### **Bot Configuration:**
- [ ] Update `info.py` with new database URLs
- [ ] Update database names
- [ ] Test database connections

### **Content Setup:**
- [ ] Upload test movies to channels
- [ ] Add movie records to database
- [ ] Test movie sending
- [ ] Verify subtitles work

### **Testing:**
- [ ] Test movie search
- [ ] Test language selection  
- [ ] Test channel subscription
- [ ] Test movie + subtitle delivery

## 🎯 **Timeline:**

- **Database setup**: 30 minutes
- **Bot configuration**: 15 minutes  
- **Upload 10 test movies**: 2-3 hours
- **Full testing**: 1 hour

**Total: 4-5 hours for complete setup**

## 💡 **Pro Tips:**

1. **Start small** - 10 movies for testing
2. **Test thoroughly** - Each movie should work
3. **Backup databases** - Regular backups
4. **Monitor usage** - Track database size
5. **Scale gradually** - Add movies over time

---

**Result: Your own independent movie bot with subtitle support! 🎬**