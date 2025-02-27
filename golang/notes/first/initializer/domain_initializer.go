package initializer

import (
	"first/post/entity" // entity 패키지 import
	"first/post/repository"
	"first/post/service"
	"fmt"
	"os"

	"github.com/google/wire"
	"github.com/joho/godotenv"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var PostSet = wire.NewSet(
	NewPostService,
	NewPostRepository,
)

// NewPostService 생성자 함수
func NewPostService(postRepo repository.PostRepository) service.PostService {
	return service.NewPostService(postRepo)
}

// NewPostRepository 생성자 함수
func NewPostRepository(db *gorm.DB) repository.PostRepository {
	return repository.NewPostRepositoryImpl(db)
}

// DB를 초기화하고, wire를 통해 의존성을 주입하는 함수
func DomainInitializer() (*gorm.DB, error) {
	// .env 파일 로딩
	if err := godotenv.Load(); err != nil {
		return nil, fmt.Errorf("Error loading .env file")
	}

	// MySQL 연결 설정
	dbUser := os.Getenv("DB_USER")
	dbPassword := os.Getenv("DB_PASSWORD")
	dbHost := os.Getenv("DB_HOST")
	dbPort := os.Getenv("DB_PORT")
	dbName := os.Getenv("DB_NAME")
	dbCharset := os.Getenv("DB_CHARSET")
	dbLoc := os.Getenv("DB_LOC")

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=%s&parseTime=True&loc=%s", dbUser, dbPassword, dbHost, dbPort, dbName, dbCharset, dbLoc)
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, fmt.Errorf("Error connecting to the database: %v", err)
	}

	// 테이블 마이그레이션
	// repository.Post가 아니라 entity.Post로 수정
	if err := db.AutoMigrate(&entity.Post{}); err != nil {
		return nil, fmt.Errorf("Failed to auto-migrate: %v", err)
	}

	return db, nil
}
