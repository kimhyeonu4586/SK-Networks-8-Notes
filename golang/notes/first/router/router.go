package router

import (
	"first/post/controller"
	"first/post/repository"
	"first/post/service"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// RegisterPostRoutes는 게시글 관련 모든 라우트를 등록하는 함수입니다.
func RegisterPostRoutes(app *fiber.App, db *gorm.DB) {
	// DB를 기반으로 Repository 생성
	postRepo := repository.NewPostRepositoryImpl(db)
	// Repository를 기반으로 Service 생성
	postService := service.NewPostService(postRepo)

	// Controller 생성
	postController := controller.NewPostController(postService)

	// 라우트 등록
	app.Post("/posts", postController.CreatePost)
	app.Get("/posts/:id", postController.GetPostByID)
	app.Get("/posts", postController.GetAllPosts)
	app.Put("/posts/:id", postController.UpdatePost)
	app.Delete("/posts/:id", postController.DeletePost)
}

// RegisterRoutes는 모든 도메인(게시글 등)의 라우트를 등록합니다.
func RegisterRoutes(app *fiber.App, db *gorm.DB) {
	RegisterPostRoutes(app, db)
}
