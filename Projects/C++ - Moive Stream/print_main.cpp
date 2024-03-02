//
// Created by 24565 on 6/1/2022.
//

#include "RecommendationSystemLoader.h"
#include "UsersLoader.h"

int main(){
  auto rs = RecommendationSystemLoader::create_rs_from_movies ("../presubmit"
                                                               ".in_m5");
  std::vector<User> user = UsersLoader::create_users ("../presubmit.in_u5",
                                                      std::move (rs));
  if (user[0].get_recommendation_by_content ()->get_name () != "TheSilence"
      || user[2].get_recommendation_by_content ()->get_name () !=
         "HighandLow" ||
      user[4].get_recommendation_by_content ()->get_name () != "CityLights" ||
      user[6].get_recommendation_by_content ()->get_year () != 1992 ||
      user[14].get_recommendation_by_content ()->get_name () != "Casablanca")
  {
    std::cout
        << "get_recommendation_by_content from User didn't return the correct output (only negative scores)"
        << std::endl;
  }
}