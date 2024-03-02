#include "RecommendationSystem.h"
#include <cmath>
double scalar_multiple(std::vector<double>& v1, std::vector<double>& v2){
  double sum = 0;
  // Move each index i in the vectors and multiple between them.
  for (std::size_t i=0; i < v1.size(); i++){
    sum += (v1[i] * v2[i]);
  }
  return sum;
}

double nor_vector(std::vector<double>& v){
  double sum = 0;
  // Move each index of the vector and calculate the square of it.
  for (auto& num: v){
    sum += (num * num);
  }
  return sqrt (sum);
}

double similtary_func(std::vector<double>& v1, std::vector<double>& v2){
  return ((scalar_multiple (v1,v2))/(nor_vector(v1) * nor_vector (v2)));
}

bool sort_by_double(const std::pair<sp_movie, double>& pair1, const
std::pair<sp_movie , double>& pair2){
  return pair1.second > pair2.second;
}

RecommendationSystem::RecommendationSystem (){
  num_of_features = 0;
}


sp_movie RecommendationSystem::add_movie(const std::string& name,int year,
                   const std::vector<double>& features){
  // Initialize a new pointer to movie and insert it to the map system.
  sp_movie movie = std::make_shared<Movie>(name, year);
  auto new_vector = std::make_shared<std::vector<double>>(features);
  if (data_system == nullptr){
    data_system = std::make_shared<movie_map>(&sp_movie_sizes);
  }
  (*data_system)[movie] = new_vector;
  num_of_features = features.size();
  return get_movie (name, year);
}

sp_movie RecommendationSystem::recommend_by_content(const User& user){
  rank_map user_ranks = user.get_ranks();
  // Part 1: normalization of the ranks.
  double sum = 0;
  for (const auto& pair: user_ranks){
    sum += pair.second; // Sum all the ranks in the rank map.
  }
  double average =  sum / user_ranks.size();
  for (auto& pair: user_ranks){
    pair.second = pair.second - average;//Update the ranks after normalization
  }
  // Part 2: create the vector from movie features.
  // Initialize a new vector and calculate the average of each feature.
  std::vector<double> result(num_of_features, 0.0);
  for (std::size_t i=0; i < num_of_features; i++){
    for (const auto& pair: user_ranks){
      result[i] += pair.second * data_system->find(pair.first)->second->at (i);
    }
  }
  // Part 3: Search for the best movie.
  double max = MIN_VALUE; // Value update
  sp_movie best_movie = nullptr; // Movie update
  // Moves all over the movies in system and looking for movies that the
  // user did not rank, for every movie calculate how much it similar to the
  // average vector from part 2.
  for (auto& pair: (*data_system)){
    if (user_ranks.count (pair.first) == 0){
      double cur = similtary_func(result,*(pair.second));
      if (cur > max){ // If we find better movie so update.
        max = cur;
        best_movie = pair.first;
      }
    }
  }
  return best_movie;
}

double RecommendationSystem::predict_movie_score(const User &user, const
sp_movie &movie,int k){
  //Part 1: create a new vector that contain each similarity value between a
  // movie from the ranked list of user to the new movie.
  std::vector<std::pair<sp_movie, double>> movie_similtary;
  for (const auto& pairs: user.get_ranks()){
    double cur_similtary = similtary_func ((*(*data_system)[pairs.first]),
                                           (*(*data_system)[movie]));
    std::pair<sp_movie, double> new_pair = std::make_pair (pairs.first,
                                                             cur_similtary);
    movie_similtary.push_back (new_pair);
  }
  // Sort the vector from high to low to catch the best k movies.
  if (movie_similtary.size() > 1){
    std::sort (movie_similtary.begin(), movie_similtary.end(), sort_by_double);
  }
  // Part 2: calculate the rank of the new movie from the best k movie.
  double sum = 0;
  int counter1 = 0;
  // Loop that calculate the sum of all similarity values of the best k movies.
  for (const auto& pair: movie_similtary){
    if  (counter1 >= k){
      break;
    }
    sum += pair.second;
    counter1++;
  }
  double rank_result = 0;
  int counter2 =0;
  // Loop that calculate for each movie the rank of the user gave to, with the
  // similtary value to the new movie.
  for (const auto& pair: movie_similtary){
    if (counter2 >= k){
      break;
    }
    double user_rank = user.get_ranks().find (pair.first)->second;
    rank_result += pair.second * user_rank;
    counter2++;
  }
  double result = rank_result / sum;
  return result;
}

sp_movie RecommendationSystem::recommend_by_cf(const User& user, int k){
  // Create new vector of all the new movies with the predicted rank.
  std::vector<std::pair<sp_movie, double>> movies_rank;
  rank_map all_movies_ranked = user.get_ranks();
  for (auto& pair: (*data_system)){
    auto it = all_movies_ranked.find (pair.first);
    if (it == all_movies_ranked.end()){ //Checks if the user watched the movie.
      //If the user didn't watch it, get the predicted rank and add the new
      // movie to the vector with the new rank.
      double rank = predict_movie_score (user, pair.first, k);
      std::pair<sp_movie, double> new_movie = std::make_pair (pair.first,
                                                              rank);
      movies_rank.push_back (new_movie);
    }
  }
  // Sort from high rank to low and return the first movie.
  std::sort (movies_rank.begin(), movies_rank.end(), sort_by_double);
  return movies_rank[0].first;
}

sp_movie RecommendationSystem::get_movie(const std::string &name, int
year)
const{
  // Create a temporary shared pointer to use for searching
  sp_movie movie_to_find = std::make_shared<Movie>(name, year);
  auto const it = data_system->find(movie_to_find);
  if (it == data_system->end()) {
    return nullptr;
  }
  // The movie was found in the map, return the shared pointer to it
  return it->first;
}

std::ostream& operator<<(std::ostream& s, const RecommendationSystem& rs){
  for (auto& pair: *(rs.data_system)){
    s << (*pair.first);
  }
  s << "\n";
  return s;
}
