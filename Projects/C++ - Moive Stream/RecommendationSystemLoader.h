
#ifndef RECOMMENDATIONSYSTEMLOADER_H
#define RECOMMENDATIONSYSTEMLOADER_H
#include "RecommendationSystem.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#define YEAR_SEPARATOR '-'
#define MIN_FEATURE_VALUE 1.00
#define MAX_FEATURE_VALUE 10.00
class RecommendationSystemLoader {

 private:

 public:
  RecommendationSystemLoader () = delete;
  /**
   * loads movies by the given format for movies with their feature's score
   * @param movies_file_path a path to the file of the movies
   * @return smart pointer to a RecommendationSystem which was created with
   * those movies
   */
  static std::unique_ptr<RecommendationSystem> create_rs_from_movies
	  (const std::string &movies_file_path) noexcept (false);
};
#endif //RECOMMENDATIONSYSTEMLOADER_H
